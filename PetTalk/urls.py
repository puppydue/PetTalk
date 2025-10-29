from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Include forum URLs
    path('forum/', include('forum.urls')),
]
