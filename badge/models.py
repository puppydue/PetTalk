# badge/models.py
from django.db import models
from django.contrib.auth.models import User


class Badge(models.Model):
    # --- Các lựa chọn cho màu sắc và loại danh hiệu ---
    COLOR_CHOICES = [
        ("gold", "Vàng"),
        ("blue", "Xanh dương"),
        ("green", "Xanh lá"),
        ("red", "Đỏ"),
        ("cyan", "Xanh ngọc"),
        ("lime", "Xanh nhạt"),
    ]

    TYPE_CHOICES = [
        ("post", "Bài viết"),
        ("comment", "Bình luận"),
        ("reaction", "Tương tác"),
    ]

    # --- Trường dữ liệu chính ---
    name = models.CharField(max_length=100, verbose_name="Tên danh hiệu")
    description = models.TextField(verbose_name="Mô tả danh hiệu", blank=True)

    icon = models.CharField(
        max_length=5,
        default="🏆",
        verbose_name="Icon danh hiệu",
        help_text="Chọn icon hiển thị cho danh hiệu."
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="post",
        verbose_name="Loại danh hiệu",
        help_text="Chọn loại hành động dùng để tính tiến trình (bài viết, bình luận, tương tác)",
    )
    target = models.PositiveIntegerField(
        default=1,
        verbose_name="Mục tiêu cần đạt",
        help_text="Số lượng cần đạt để hoàn thành danh hiệu",
    )

    color = models.CharField(
        max_length=20,
        choices=COLOR_CHOICES,
        default="blue",
        verbose_name="Màu hiển thị",
    )

    # --- Metadata ---
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    achieved_count = models.IntegerField(default=0, verbose_name="Số người đã đạt")

    def __str__(self):
        return self.name


class UserBadgeProgress(models.Model):
    """
    Tiến trình danh hiệu của từng user cho từng badge.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="badge_progress"
    )
    badge = models.ForeignKey(
        Badge,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="user_progress"
    )

    post_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    reaction_count = models.PositiveIntegerField(default=0)

    progress = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "badge")

    def __str__(self):
        return f"{self.user.username} - {self.badge.name if self.badge else 'No badge'}"

    def update_progress(self, save=True):
        """
        Cập nhật self.progress dựa trên loại badge (post/comment/reaction).
        """
        if not self.badge:
            return

        if self.badge.type == "post":
            self.progress = self.post_count
        elif self.badge.type == "comment":
            self.progress = self.comment_count
        elif self.badge.type == "reaction":
            self.progress = self.reaction_count

        if save:
            self.save(update_fields=["progress", "last_updated"])
