from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from designSpace.accounts.forms import CustomUserCreationForm
from designSpace.projects.models import Project

UserModel = get_user_model()

class UserRegisterView(CreateView):
    model = UserModel
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            login(self.request, self.object)
            messages.success(self.request, "Registration successful! You are now logged in.")
        except Exception as e:
            messages.error(self.request, "An error occurred during login.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Welcome to DesignSpace!"
        return context


class UserLoginView(LoginView):
    template_name = "accounts/log-in.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Welcome back to DesignSpace!"
        return context


class ProfileView(ListView):
    model = Project
    template_name = 'accounts/profile-details-page.html'
    context_object_name = 'projects'

    # paginate_by = 6

    def get_queryset(self):
        return Project.objects.filter(creator=self.request.user).order_by('-created_at')