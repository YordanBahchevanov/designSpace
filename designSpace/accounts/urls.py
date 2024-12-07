from django.contrib.auth.views import LogoutView
from django.urls import path, include

from designSpace.accounts import views
from designSpace.accounts.views import UserRegisterView, UserLoginView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='log-in'),
    path('logout/', LogoutView.as_view(), name='log-out'),
    path('profile/<int:pk>/', include([
        path('', views.ProfileDetailsView.as_view(), name='profile-details'),
        path('edit/', views.ProfileUpdateView.as_view(), name='profile-edit'),
        path('delete/', views.ProfileDeleteView.as_view(), name='profile-delete'),
    ]))
]
