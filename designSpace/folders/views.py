from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AddProjectToFolderForm
from .models import Folder
from ..projects.models import Project


class FolderCreateView(LoginRequiredMixin, CreateView):
    model = Folder
    fields = ['title']
    template_name = 'folders/create-folder.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_pk'] = self.request.user.pk

        return context


class AddProjectToFolderView(FormView):
    template_name = 'folders/add-project-to-folder.html'  # Define the template
    form_class = AddProjectToFolderForm  # Define the form class
    success_url = reverse_lazy('home')  # Define a default success URL (not strictly necessary here)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass the logged-in user to the form so the form knows which user it's dealing with
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Get the project based on the project_id from the URL
        project = Project.objects.get(id=self.kwargs['project_id'])

        # Get the existing folder or create a new folder if a new folder title is provided
        folder = form.cleaned_data.get('folder')
        new_folder_title = form.cleaned_data.get('new_folder_title')

        if new_folder_title:
            # Create a new folder if a title is provided
            folder = Folder.objects.create(title=new_folder_title, user=self.request.user)

        # Add the project to the folder
        folder.projects.add(project)

        # Redirect to the project's detail page (or any other page you prefer)
        return redirect(reverse_lazy('projects:project-details', args=[project.slug]))

    def form_invalid(self, form):
        # If the form is invalid, re-render the page with errors
        return self.render_to_response({'form': form})
