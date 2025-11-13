# badge/urls.py
from django.urls import path
from . import views

app_name = 'badge'

urlpatterns = [
    # USER SIDE
    path('', views.user_badges, name='user_badges'),
    path('badges/save-display/', views.save_display_badge, name='save_display_badge'),

    # ADMIN SIDE
    path('admin/', views.admin_badges, name='admin_badges'),
    path('admin/add/', views.add_badge, name='add_badge'),
    path('admin/<int:badge_id>/edit/', views.edit_badge, name='edit_badge'),
    path('admin/<int:badge_id>/delete/', views.delete_badge, name='delete_badge'),
]
