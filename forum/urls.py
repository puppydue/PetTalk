from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.create_post, name='create_post'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/react/<str:react_type>/', views.toggle_reaction, name='toggle_reaction'),
    path('<int:post_id>/report/', views.report_post, name='report_post'),
]
