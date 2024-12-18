from django.urls import path, include

from designSpace.folders import views


urlpatterns = [
    path('create-folder/', views.FolderCreateView.as_view(), name='create-folder'),
    path('add-to-folder/<int:project_id>/', views.AddProjectToFolderView.as_view(), name='add-project-to-folder'),
    # path('article/<int:pk>/', include([
    #     path('', views.ArticleDetailsView.as_view(), name='article-details'),
    #     path("edit/", views.ArticleUpdateView.as_view(), name="article-edit"),
    #     path('delete/', views.ArticleDeleteView.as_view(), name='article-delete'),
    # ]))
]