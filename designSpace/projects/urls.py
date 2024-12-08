from django.urls import path, include
from rest_framework.routers import DefaultRouter

from designSpace.projects import views

app_name = 'projects'

# router = DefaultRouter()
# router.register('', ProjectViewSet)

urlpatterns = [
    path('api/', views.ListProjectView.as_view(), name='projects-list'),
    path('create-project/', views.ProjectCreateView.as_view(), name='create-project'),
    path('project/<slug:slug>/', include([
        path('', views.ProjectDetailsView.as_view(), name='project-details'),
        # path('edit/', views.PetEditPage.as_view(), name='edit-pet'),
        # path('delete/', views.PetDeletePage.as_view(), name='delete-pet'),
    ]))
]