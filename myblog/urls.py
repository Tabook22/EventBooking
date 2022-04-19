from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('myvideos.urls')),
    path('members/',include('django.contrib.auth.urls')),
    path('members/',include('members.urls')),
    path('videos/',include('myvideos.urls')),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
