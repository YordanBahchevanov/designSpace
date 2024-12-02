from django.urls import path, include
from rest_framework.routers import DefaultRouter

from designSpace.projects import views

app_name = 'projects'

# router = DefaultRouter()
# router.register('', ProjectViewSet)

urlpatterns = [
    path('api/', views.ListProjectView.as_view(), name='projects-list'),
    path('create-project/', views.ProjectCreateView.as_view(), name='create-project'),
]