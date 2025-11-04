from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ phê duyệt'),
        ('approved', 'Đã phê duyệt'),
        ('rejected', 'Từ chối'),
    ]

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    date = models.DateTimeField(verbose_name="Thời gian bắt đầu")
    end_date = models.DateTimeField(verbose_name="Thời gian kết thúc", null=True, blank=True)
    location = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='event_covers/', blank=True, null=True)
    capacity = models.PositiveIntegerField(default=50)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    participants = models.ManyToManyField(User, blank=True, related_name='joined_events')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)

    def __str__(self):
        return self.title


class Event_Registration(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ duyệt'),
        ('approved', 'Đã duyệt'),
        ('rejected', 'Từ chối'),
    ]

    event_regis_id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.username.username} - {self.event.title}"
