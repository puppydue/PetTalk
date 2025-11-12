# badges/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_badges, name='user_badges'),
    path('save_badge/', views.save_display_badge, name='save_display_badge'),  # ← THÊM DÒNG NÀY
]