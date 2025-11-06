from django.urls import path
from .views import user_badges

app_name = "badges"
urlpatterns = [
    path("", user_badges, name="user_badges"),
]
