# badges/models.py
from django.db import models
from django.contrib.auth.models import User
from badge.models import Badge  # Import Badge chính từ app badge

class UserBadgeProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, null=True, blank=True)  # Đã reference đúng 'badge.Badge', nhưng remove null/blank=True để strict hơn nếu có thể (sau migrate)

    post_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    reaction_count = models.PositiveIntegerField(default=0)
    progress = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def update_progress(self):
        """Cập nhật tiến trình dựa trên loại badge."""
        if self.badge.type == "post":
            self.progress = self.post_count
        elif self.badge.type == "comment":
            self.progress = self.comment_count
        elif self.badge.type == "reaction":
            self.progress = self.reaction_count
        # Thêm if cho type mới nếu cần (event/adoption)
        self.save()