from django.urls import path

from designSpace.common import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('ajax/search/', views.ajax_search_projects, name='ajax-search-projects'),
    path('about/', views.AboutView.as_view(), name='about'),
]