from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth_slider, name='login'),
]
