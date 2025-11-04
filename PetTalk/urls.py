from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🌐 Forum app
    path('forum/', include('forum.urls')),

    # Hệ thống xác thực
    path('', include('accounts.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),


    # 🎉 Events app
    path('events/', include('Events.urls')),
    path('badge/', include('badge.urls')),
    path('moderation/', include('moderation.urls')),

]

# 🖼️ Chỉ bật khi đang DEV để hiển thị ảnh từ media/
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
