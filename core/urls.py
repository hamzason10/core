from app import views
from django.contrib import admin
from django.urls import path
from .settings import MEDIA_ROOT,MEDIA_URL
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('enroll/', views.face_enroll),
    path('detect/', views.face_detection),
]
urlpatterns += static(MEDIA_URL,document_root=MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
