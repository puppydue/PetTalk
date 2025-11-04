from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.moderation_reports, name='moderation_reports'),
    path('reports/<str:report_type>/<int:report_id>/', views.report_detail, name='report_detail'),
    path('reports/<str:report_type>/<int:report_id>/action/', views.report_action, name='report_action'),

    path('events/', views.moderation_events, name='moderation_events'),
    path('events/<int:regis_id>/', views.event_detail, name='event_detail'),
    path('events/<int:regis_id>/action/', views.event_action, name='event_action'),
    path('events/update/<int:event_id>/', views.update_event_status, name='update_event_status'),
]
