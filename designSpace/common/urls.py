from django.urls import path

from designSpace.common import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('ajax/search/', views.SearchView.as_view(), name='ajax_search'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('project/<int:project_id>/like/', views.like_project, name='like-project'),
]