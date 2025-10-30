from django.db import models
from django.contrib.auth.models import User

# ==============================
# 1️⃣ BẢNG POST — Bài viết
# ==============================
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    topic = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bài viết"
        verbose_name_plural = "Danh sách bài viết"

    def __str__(self):
        return f"{self.title} - {self.username}"


# ==============================
# 2️⃣ BẢNG COMMENT — Bình luận
# ==============================
class Comment(models.Model):
    cmt_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = "Bình luận"
        verbose_name_plural = "Danh sách bình luận"

    def __str__(self):
        return f"Comment by {self.username} on {self.post}"


# ==============================
# 3️⃣ BẢNG REACTION — Cảm xúc bài viết
# ==============================
class Reaction(models.Model):
    REACT_CHOICES = [
        ('upvote', 'upvote'),
        ('downvote', 'downvote'),

    ]

    react_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    reacted_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=REACT_CHOICES)

    class Meta:
        unique_together = ('username', 'post')  # Mỗi người chỉ được 1 reaction / post
        verbose_name = "Bình chọn"
        verbose_name_plural = "Danh sách bình chọn"

    def __str__(self):
        return f"{self.username} reacted {self.type} on {self.post}"


# ==============================
# 4️⃣ BẢNG POSTS_IMAGE — Hình ảnh trong bài viết
# ==============================
class PostsImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/')
    order = models.PositiveIntegerField(default=0, help_text="Thứ tự hiển thị ảnh trong bài viết")

    class Meta:
        ordering = ['order']
        verbose_name = "Hình ảnh bài viết"
        verbose_name_plural = "Danh sách hình ảnh"

    def __str__(self):
        return f"Ảnh {self.image_id} của bài {self.post.title}"
