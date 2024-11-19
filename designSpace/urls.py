from django.contrib import admin
from django.shortcuts import render
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: render(request, 'common/home.html'), name='home'),
]
