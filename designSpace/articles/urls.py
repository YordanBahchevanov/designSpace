from django.urls import path, include
from rest_framework.routers import DefaultRouter

from designSpace.articles.views import ArticleViewSet
from designSpace.articles import views

app_name = 'articles'

router = DefaultRouter()
router.register('', ArticleViewSet)

urlpatterns = [
    path('api/articles/', include(router.urls)),
    path('create-article/', views.ArticleCreateView.as_view(), name='create-article'),
    path('article/<int:pk>/', include([
        path('', views.ArticleDetailsView.as_view(), name='article-details'),
        path("edit/", views.ArticleUpdateView.as_view(), name="article-edit"),
        path('delete/', views.ArticleDeleteView.as_view(), name='article-delete'),
    ]))
]