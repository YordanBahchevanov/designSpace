import cloudinary
from asgiref.sync import sync_to_async
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from designSpace.accounts.forms import CustomUserCreationForm, ProfileEditForm
from designSpace.accounts.models import Profile
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
        num_projects = context['projects'].count()
        context['empty_slots'] = max(6 - num_projects, 0)

        context['profile'] = get_object_or_404(Profile, user__pk=self.kwargs['pk'])
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def form_valid(self, form):

        if self.request.POST.get('remove_profile_picture') and self.object.profile_picture:
            public_id = self.object.profile_picture.public_id
            cloudinary.uploader.destroy(public_id)

            self.object.profile_picture = None
            self.object.save()

        form.save()

        messages.success(self.request, "Your profile has been updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={
                'pk': self.request.user.pk,
            }
        )


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = "accounts/profile-delete.html"
    success_url = reverse_lazy("home")  # Redirect to home page after deletion

    def get_object(self, queryset=None):
        """Ensure only the logged-in user's profile can be deleted."""
        return get_object_or_404(Profile, user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Your profile has been deleted successfully.")
        return super().delete(request, *args, **kwargs)