from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("", views.my_profile, name="my_profile"),
    path("pet/add/", views.pet_create, name="pet_add"),
    path("pet/<int:pk>/edit/", views.pet_update, name="pet_edit"),
]
