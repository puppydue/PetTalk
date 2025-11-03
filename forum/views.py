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

from django.shortcuts import render, redirect
from .models import Post  # <-- 1. PHẢI IMPORT POST

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post

@login_required
def forum_view(request):
    if request.method == 'POST':
        # Xử lý tạo bài viết nếu có
        pass

    post_list = Post.objects.all()

    context = {
        'posts': post_list,
        'topic_choices': Post.TOPIC_CHOICES
    }

    return render(request, 'forum/post_list.html', context)
