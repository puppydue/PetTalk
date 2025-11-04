from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Event(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ phê duyệt'),
        ('approved', 'Đã phê duyệt'),
        ('rejected', 'Từ chối'),
    ]

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    # ⏰ Thời gian bắt đầu và kết thúc
    date = models.DateTimeField(verbose_name="Thời gian bắt đầu")
    end_date = models.DateTimeField(verbose_name="Thời gian kết thúc", null=True, blank=True)

    location = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='event_covers/', blank=True, null=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)

    capacity = models.PositiveIntegerField(default=50)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    participants = models.ManyToManyField(User, blank=True, related_name='joined_events')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    # ==============================
    # 🧩 KIỂM TRA RÀNG BUỘC HỢP LỆ
    # ==============================
    def clean(self):
        """Ràng buộc logic: Ngày kết thúc không được trước ngày bắt đầu."""
        if self.end_date and self.date and self.end_date < self.date:
            raise ValidationError("⛔ Thời gian kết thúc không được trước thời gian bắt đầu.")

    # ==============================
    # 🕓 HÀM KIỂM TRA SỰ KIỆN ĐÃ KẾT THÚC CHƯA
    # ==============================
    def is_past(self):
        """Trả về True nếu sự kiện đã kết thúc."""
        return self.end_date and self.end_date < timezone.now()

    def is_ongoing(self):
        """Trả về True nếu sự kiện đang diễn ra."""
        now = timezone.now()
        return self.date <= now <= (self.end_date or now)

    def __str__(self):
        return self.title
