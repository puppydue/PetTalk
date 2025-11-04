from django.db import models
from django.contrib.auth.models import User
from datetime import date

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_image = models.ImageField(upload_to="avatars/", blank=True, null=True)
    role = models.CharField(max_length=50, default="Thành viên")
    phone = models.CharField(max_length=20, blank=True)
    birthdate = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f"UserProfile: {self.user.username}"

class PetProfile(models.Model):
    SEX_CHOICES = (('M', 'Đực'), ('F', 'Cái'))

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pets")
    name = models.CharField(max_length=100)
    avatar_image = models.ImageField(upload_to="pets/", blank=True, null=True)
    species = models.CharField(max_length=50)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)
    birthdate = models.DateField(blank=True, null=True)
    color = models.CharField(max_length=60, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def age_years(self):
        """Tính tuổi theo công thức: 6 tháng = 0.5 tuổi"""
        if not self.birthdate:
            return None
        today = date.today()
        delta = (today.year - self.birthdate.year) * 12 + (today.month - self.birthdate.month)
        # Chuyển số tháng sang năm (mỗi 6 tháng = 0.5 tuổi)
        return round(delta / 12, 1)

    def __str__(self):
        return f"{self.name} ({self.user.username})"
