from django.urls import path
from . import views

app_name = 'badge'

urlpatterns = [
    path('admin_badges/', views.admin_badges, name='admin_badges'),
    path('admin_badges/add/', views.add_badge, name='add_badge'),
    path('admin_badges/edit/<int:badge_id>/', views.edit_badge, name='edit_badge'),
    path('admin_badges/delete/<int:badge_id>/', views.delete_badge, name='delete_badge'),
]

