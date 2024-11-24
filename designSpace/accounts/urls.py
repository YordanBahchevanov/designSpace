from django.contrib.auth.views import LogoutView
from django.urls import path

from designSpace.accounts.views import UserRegisterView, UserLoginView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='log-in'),
    path('logout/', LogoutView.as_view(), name='log-out'),
]