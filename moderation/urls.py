from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.moderation_reports, name='moderation_reports'),
    path('reports/update/<str:rtype>/<int:rid>/', views.update_report_status, name='update_report_status'),

    path('events/', views.moderation_events, name='moderation_events'),
    path('events/<int:regis_id>/action/', views.event_action, name='event_action'),
    path('events/update/<int:event_id>/', views.update_event_status, name='update_event_status'),
    path('stats/', views.moderation_stats, name='moderation_stats'),
    path("keywords/", views.moderation_keywords, name="moderation_keywords"),
    path("keywords/delete/<int:pk>/", views.delete_keyword, name="delete_keyword"),

]
