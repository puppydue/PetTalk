from django.db import models
from django.contrib.auth.models import User


# ============================
# 1️⃣ BẢNG POST
# ============================
class Post(models.Model):
    TOPIC_CHOICES = [
        ('chamsoc', 'Chăm sóc thú cưng'),
        ('dinhduong', 'Dinh dưỡng'),
        ('huanluyen', 'Huấn luyện'),
        ('capcuu', 'Cấp cứu'),
    ]

    post_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.username}"

    def total_votes(self):
        ups = self.reactions.filter(type='upvote').count()
        downs = self.reactions.filter(type='downvote').count()
        return ups - downs

    def user_reaction(self, user):
        try:
            reaction = self.reactions.get(username=user)
            return reaction.type
        except:
            return None


# ============================
# 2️⃣ ẢNH TRONG BÀI VIẾT
# ============================
class PostsImage(models.Model):
    # ❌ bỏ dòng: image_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/')
    order = models.PositiveIntegerField(default=0, help_text="Thứ tự hiển thị ảnh trong bài viết")

    class Meta:
        ordering = ['order']
        verbose_name = "Hình ảnh bài viết"
        verbose_name_plural = "Danh sách hình ảnh"

# ============================
# 3️⃣ REACTION (UP/DOWN VOTE)
# ============================
class Reaction(models.Model):
    REACT_CHOICES = [
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote')
    ]
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    type = models.CharField(max_length=20, choices=REACT_CHOICES)
    reacted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('username', 'post')

    def __str__(self):
        return f"{self.username} {self.type} {self.post}"


# ============================
# 4️⃣ COMMENT
# ============================
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.username}: {self.content[:40]}"


# ============================
# 5️⃣ REPORT (BÁO CÁO)
# ============================
class ReportsPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Report {self.post} by {self.reporter}"
