from cloudinary.uploader import upload, destroy

from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from designSpace.accounts.forms import CustomUserCreationForm, ProfileEditForm

from designSpace.accounts.models import Profile
from designSpace.accounts.utils import get_profile_image_folder
from designSpace.articles.models import Article
from designSpace.projects.models import Project

import logging


UserModel = get_user_model()

class UserRegisterView(CreateView):
    model = UserModel
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)

        user = self.object
        authenticated_user = authenticate(
            request=self.request,
            username=user.email,
            password=form.cleaned_data['password1'],
        )
        if authenticated_user:
            login(self.request, authenticated_user)
            messages.success(self.request, "Registration successful! You are now logged in.")
        else:
            messages.error(self.request, "An error occurred during login.")

        return response


class UserLoginView(LoginView):
    template_name = "accounts/log-in.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Welcome back to DesignSpace!"
        return context


class ProfileDetailsView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'accounts/profile-details.html'
    context_object_name = 'projects'
    paginate_by = 6

    def get_queryset(self):
        profile_user = get_object_or_404(Profile, user__pk=self.kwargs['pk']).user
        return Project.objects.filter(creator=profile_user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile_user = get_object_or_404(Profile, user__pk=self.kwargs['pk'])
        context['profile'] = profile_user

        context['is_own_profile'] = self.request.user == profile_user.user

        num_projects = context['projects'].count()
        context['empty_slots'] = max(self.paginate_by - num_projects, 0)

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def form_valid(self, form):
        old_profile_picture_public_id = None
        if self.object.profile_picture:
            old_profile_picture_public_id = self.object.profile_picture_public_id

        new_profile_picture = form.cleaned_data.get('profile_picture')

        if new_profile_picture:
            if hasattr(new_profile_picture, 'read'):
                upload_response = upload(
                    new_profile_picture,
                    folder=get_profile_image_folder(self.request)
                )

                if old_profile_picture_public_id:
                    try:
                        destroy(old_profile_picture_public_id)
                    except Exception as e:
                        messages.error(self.request, f"Error deleting old image: {e}")

                self.object.profile_picture = upload_response['secure_url']
                self.object.profile_picture_public_id = upload_response['public_id']
            else:
                messages.error(self.request, 'The uploaded file is not valid.')

        response = super().form_valid(form)

        messages.success(self.request, 'Your profile has been updated successfully.')

        return response

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.request.user.pk})



class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = "accounts/profile-delete.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Your profile has been deleted successfully.")
        return super().delete(request, *args, **kwargs)


class ProfileArticlesView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'accounts/profile-articles.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self):
        profile_user = get_object_or_404(Profile, user__pk=self.kwargs['pk']).user
        return Article.objects.filter(author=profile_user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile_user = get_object_or_404(Profile, user__pk=self.kwargs['pk']).user
        is_writer = profile_user.groups.filter(name='Writer').exists()
        context['is_writer'] = is_writer
        print(f"Is Writer: {is_writer}")  # Debugging line
        print(f"User: {profile_user.username}, Groups: {[group.name for group in profile_user.groups.all()]}")

        context['profile'] = profile_user.profile
        context['is_own_profile'] = self.request.user == profile_user

        num_articles = context['articles'].count()
        context['empty_slots'] = max(self.paginate_by - num_articles, 0)

        return context