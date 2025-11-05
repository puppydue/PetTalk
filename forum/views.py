from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from .models import Post, Reaction, Comment, ReportsPost, PostsImage
from .forms import PostForm, CommentForm, ReportForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Comment
from django.utils.html import linebreaks, escape
from django.views.decorators.http import require_POST



# ========== 🧭 DANH SÁCH BÀI VIẾT ==========
@login_required
def post_list(request):
    q = request.GET.get('q')
    topic = request.GET.get('topic')
    posts = Post.objects.prefetch_related('images', 'comments', 'reactions')

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
        'topic_choices': Post.TOPIC_CHOICES
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
            # xử lý ảnh nếu có
            for img in request.FILES.getlist('images'):
                PostsImage.objects.create(post=post, image=img)
            return redirect('forum:post_list')
    return redirect('forum:post_list')


# ========== 💬 XEM CHI TIẾT + COMMENT ==========
@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()
    comment_form = CommentForm()
    report_form = ReportForm()

    if request.method == 'POST' and 'comment' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            cmt = comment_form.save(commit=False)
            cmt.username = request.user
            cmt.post = post
            cmt.save()
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
            reaction.delete()  # gỡ vote
        else:
            reaction.type = react_type
            reaction.save()
    else:
        reaction.type = react_type
        reaction.save()

    total = post.total_votes()
    return JsonResponse({'total_votes': total})


# ========== 🚨 BÁO CÁO BÀI VIẾT ==========
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
def toggle_reaction(request, post_id, react_type):
    # ... (giữ nguyên logic toggle_reaction)
    post = get_object_or_404(Post, pk=post_id)
    reaction, created = Reaction.objects.get_or_create(username=request.user, post=post)
    if not created:
        if reaction.type == react_type:
            # click lại cùng nút => bỏ vote
            reaction.delete()
        else:
            reaction.type = react_type
            reaction.save()
    else:
        reaction.type = react_type
        reaction.save()

    total = post.total_votes()
    current = post.reactions.filter(username=request.user).first()
    current_type = current.type if current else None
    return JsonResponse({'total_votes': total, 'reaction': current_type})


# ===== SỬA LỖI Ở ĐÂY =====

@login_required
def edit_comment(request, id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=id)
        data = json.loads(request.body)

        if comment.username == request.user:
            comment.content = data.get('content', '').strip()
            comment.save()

            # An toàn: escape để chống XSS, linebreaks để xuống dòng
            new_content_html = linebreaks(escape(comment.content))

            return JsonResponse({
                'status': 'ok',
                'new_content_html': new_content_html
            })
        else:
            return JsonResponse({'status': 'forbidden'}, status=403)

    return JsonResponse({'status': 'error'}, status=400)

@login_required
@require_POST
def delete_comment(request, id):
    comment = get_object_or_404(Comment, pk=id, username=request.user)
    comment.delete()
    return JsonResponse({'status': 'deleted'})