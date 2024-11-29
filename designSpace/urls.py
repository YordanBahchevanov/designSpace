from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('designSpace.common.urls')),
    path('accounts/', include('designSpace.accounts.urls')),
    path('project/', include('designSpace.projects.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
