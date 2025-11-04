from django.contrib import admin
from .models import UserProfile, PetProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'location')

@admin.register(PetProfile)
class PetProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'species', 'sex', 'weight_kg', 'created_at')
