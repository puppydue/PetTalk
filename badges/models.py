from django.db import models
from django.contrib.auth.models import User

class Badge(models.Model):
    COLOR_CHOICES = [
        ("gold", "Vàng"),
        ("blue", "Xanh dương"),
        ("green", "Xanh lá"),
        ("red", "Đỏ"),
        ("cyan", "Xanh ngọc"),
        ("lime", "Xanh nhạt"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, default="🏅")
    target = models.IntegerField(default=1)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default="blue")

    def __str__(self):
        return self.name


class UserBadgeProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def is_completed(self):
        return self.progress >= self.badge.target
