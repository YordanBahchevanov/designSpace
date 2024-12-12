from django.urls import path, include
from rest_framework.routers import DefaultRouter

from designSpace.projects import views
from designSpace.projects.views import ProjectViewSet

app_name = 'projects'

router = DefaultRouter()
router.register('', ProjectViewSet)

urlpatterns = [
    path('api/projects/', include(router.urls)),
    path('create-project/', views.ProjectCreateView.as_view(), name='create-project'),
    path('project/<slug:slug>/', include([
        path('', views.ProjectDetailsView.as_view(), name='project-details'),
        # path('edit/', views.PetEditPage.as_view(), name='edit-pet'),
        # path('delete/', views.PetDeletePage.as_view(), name='delete-pet'),
    ]))
]