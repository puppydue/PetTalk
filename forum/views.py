from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.prefetch_related('images', 'comments', 'reactions').all()

    # Thêm dữ liệu đếm reaction cho mỗi post
    for post in posts:
        post.upvotes = post.reactions.filter(type='upvote').count()
        post.downvotes = post.reactions.filter(type='downvote').count()

    return render(request, 'forum/post_list.html', {'posts': posts})
from django.db.models import Q

def forum_view(request):
    # Lấy query tìm kiếm từ URL, nếu không có thì là chuỗi rỗng
    search_query = request.GET.get('q', '')

    if search_query:
        # Lọc các bài viết có tiêu đề (title) hoặc nội dung (content) chứa query
        # 'icontains' là không phân biệt hoa thường
        post_list = Post.objects.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        ).distinct().order_by('-created_at')
    else:
        # Nếu không tìm kiếm, lấy tất cả bài viết
        post_list = Post.objects.all().order_by('-created_at')

    # ... (các phần khác của view, ví dụ: phân trang) ...

    context = {
        'posts': post_list,
        # 'request' tự động có sẵn nếu bạn dùng RequestContext
    }
    return render(request, 'forum.html', context)