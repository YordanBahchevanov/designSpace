from django.urls import path, include

from designSpace.folders import views

# app_name = 'folders'

urlpatterns = [
    path('create-folder/', views.FolderCreateView.as_view(), name='create-folder'),
    path('add-to-folder/<int:project_id>/', views.AddProjectToFolderView.as_view(), name='add-project-to-folder'),
    path('folder/<int:pk>/', include([
        path('', views.FolderDetailsView.as_view(), name='folder-details'),
        path('remove_project/<int:project_id>/', views.remove_project_from_folder, name='remove-project-from-folder'),
    ]))
]