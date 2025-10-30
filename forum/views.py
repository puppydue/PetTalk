from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.prefetch_related('images', 'comments', 'reactions').all()

    # Thêm dữ liệu đếm reaction cho mỗi post
    for post in posts:
        post.upvotes = post.reactions.filter(type='upvote').count()
        post.downvotes = post.reactions.filter(type='downvote').count()

    return render(request, 'forum/post_list.html', {'posts': posts})