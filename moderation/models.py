from django.db import models
from django.contrib.auth.models import User
from forum.models import Reports_post, Reports_comment, Post, Comment
from Events.models import Event_Registration

class ModerationLog(models.Model):
    ACTION_CHOICES = [
        ('delete_post', 'Xóa bài viết'),
        ('delete_comment', 'Xóa bình luận'),
        ('dismiss', 'Bác bỏ báo cáo'),
        ('approve_event', 'Duyệt sự kiện'),
        ('reject_event', 'Từ chối sự kiện'),
    ]

    moderator = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    target_post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True)
    target_comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True, blank=True)
    target_registration = models.ForeignKey(Event_Registration, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.moderator.username} - {self.get_action_display()} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"
