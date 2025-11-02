from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.auth_slider, name='login'),
]
