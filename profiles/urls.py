from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("", views.my_profile, name="my_profile"),
    path("pet/add/", views.pet_create, name="pet_create"),  # ✅ cho thêm thú cưng
    path("pet/<int:pk>/update/", views.pet_update, name="pet_update"),  # ✅ cho cập nhật thú cưng
    path('pet/<int:pk>/delete/', views.pet_delete, name='pet_delete'),
    path('<str:username>/', views.view_user_profile, name='view_user_profile'),
]
