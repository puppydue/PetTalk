from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import linebreaks, escape
from django.contrib import messages
import json

# Import Models & Forms
from .models import Post, Reaction, Comment, ReportsPost, PostsImage, ReportsComment
from .forms import PostForm, CommentForm, ReportForm


# ========== 🧭 DANH SÁCH BÀI VIẾT ==========
@login_required
def post_list(request):
    q = request.GET.get('q')
    topic = request.GET.get('topic')

    posts = Post.objects.select_related('username__userprofile').prefetch_related('images', 'comments', 'reactions')

    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))
    if topic:
        posts = posts.filter(topic=topic)

    for post in posts:
        post.total_vote = post.total_votes()
    form = PostForm()

    return render(request, 'forum/post_list.html', {
        'posts': posts,
        'form': form,
        'all_topic_choices': Post.TOPIC_CHOICES
    })


# ========== ✏️ TẠO BÀI VIẾT ==========
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.username = request.user
            post.save()
            for img in request.FILES.getlist('images'):
                PostsImage.objects.create(post=post, image=img)
            return redirect('forum:post_list')
    return redirect('forum:post_list')


# ========== 💬 XEM CHI TIẾT + COMMENT (ĐÃ SỬA LOGIC REPLY) ==========
@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # 🔥 QUAN TRỌNG: Chỉ lấy comment cha (parent=None) để đệ quy
    comments = post.comments.filter(parent__isnull=True).select_related('username__userprofile').prefetch_related(
        'replies')

    comment_form = CommentForm()
    report_form = ReportForm()
    post.total_vote = post.total_votes()

    if request.method == 'POST' and 'comment' in request.POST:
        # Lấy nội dung và parent_id (nếu là reply)
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')

        if content:
            parent_cmt = None
            if parent_id:
                try:
                    parent_cmt = Comment.objects.get(id=parent_id)
                except Comment.DoesNotExist:
                    pass

            Comment.objects.create(
                post=post,
                username=request.user,
                content=content,
                parent=parent_cmt  # Lưu liên kết cha-con
            )
            return redirect('forum:post_detail', post_id=post_id)

    return render(request, 'forum/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'report_form': report_form
    })

# ========== ⚡ REACTION (UP/DOWN) ==========
@login_required
def toggle_reaction(request, post_id, react_type):
    post = get_object_or_404(Post, pk=post_id)
    reaction, created = Reaction.objects.get_or_create(username=request.user, post=post)

    if not created:
        if reaction.type == react_type:
            reaction.delete()  # Click lại thì xóa (unvote)
        else:
            reaction.type = react_type
            reaction.save()
    else:
        reaction.type = react_type
        reaction.save()

    total = post.total_votes()
    # Lấy trạng thái hiện tại để update UI
    current = None
    try:
        current_react = Reaction.objects.get(username=request.user, post=post)
        current = current_react.type
    except Reaction.DoesNotExist:
        pass

    return JsonResponse({'total_votes': total, 'reaction': current})


# ========== 🚨 BÁO CÁO ==========
@login_required
def report_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.post = post
            report.reporter = request.user
            report.save()
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})


@login_required
def report_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        details = request.POST.get('details', '')
        if ReportsComment.objects.filter(username=request.user, comment=comment).exists():
            return JsonResponse({'status': 'duplicate'})
        ReportsComment.objects.create(
            username=request.user,
            comment=comment,
            reason=reason,
            details=details,
            status='pending'
        )
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})


# ========== 🛠 QUẢN LÝ COMMENT (EDIT/DELETE) ==========
@login_required
def edit_comment(request, id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=id)
        data = json.loads(request.body)

        if comment.username == request.user:
            comment.content = data.get('content', '').strip()
            comment.save()
            new_content_html = linebreaks(escape(comment.content))
            return JsonResponse({'status': 'ok', 'new_content_html': new_content_html})
        else:
            return JsonResponse({'status': 'forbidden'}, status=403)
    return JsonResponse({'status': 'error'}, status=400)


@login_required
@require_POST
def delete_comment(request, id):
    comment = get_object_or_404(Comment, pk=id, username=request.user)
    comment.delete()
    return JsonResponse({'status': 'deleted'})


# ========== 🛠 QUẢN LÝ BÀI VIẾT ==========
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, username=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post = form.save()  # Lưu title, content, topic trước

            # 1. XÓA ẢNH CŨ (nếu người dùng bấm X)
            delete_ids = request.POST.getlist('delete_images')  # danh sách ID ảnh cần xóa
            if delete_ids:
                PostsImage.objects.filter(id__in=delete_ids, post=post).delete()

            # 2. THÊM ẢNH MỚI
            new_images = request.FILES.getlist('images')
            for img_file in new_images:
                PostsImage.objects.create(post=post, image=img_file)

            # 3. Nếu là AJAX → trả JSON để frontend cập nhật ảnh
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({
                    "status": "ok",
                    "title": post.title,
                    "content": post.content,
                    "images": [img.image.url for img in post.images.all()],  # ← quan trọng: trả danh sách ảnh mới nhất
                })

            return redirect('profiles:my_profile')

        else:
            # Nếu form lỗi + AJAX → trả lỗi
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"status": "error", "errors": form.errors}, status=400)

    # GET request
    form = PostForm(instance=post)
    return render(request, 'forum/post_edit.html', {'form': form, 'post': post})
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, username=request.user)
    try:
        post_title = post.title
        post.delete()
        messages.success(request, f"Đã xóa bài viết '{post_title}' thành công.")
    except Exception as e:
        messages.error(request, f"Có lỗi xảy ra khi xóa: {e}")
    return redirect('profiles:my_profile')
def post_edit_data(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)

    if post.username != request.user:
        return JsonResponse({"error": "forbidden"}, status=403)

    images = [
        {"id": img.id, "url": img.image.url}
        for img in post.images.all()
    ]

    return JsonResponse({
        "title": post.title,
        "content": post.content,
        "topic": post.topic,
        "images": images,
    })
