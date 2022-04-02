from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('articles.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
