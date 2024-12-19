from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
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


class AddProjectToFolderView(LoginRequiredMixin, FormView):
    template_name = 'folders/add-project-to-folder.html'
    form_class = AddProjectToFolderForm
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('log-in')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        project = Project.objects.get(id=self.kwargs['project_id'])

        folder = form.cleaned_data.get('folder')
        new_folder_title = form.cleaned_data.get('new_folder_title')

        if new_folder_title:
            folder = Folder.objects.create(title=new_folder_title, user=self.request.user)

        folder.projects.add(project)

        return redirect(reverse_lazy('projects:project-details', args=[project.slug]))

    def form_invalid(self, form):
        return self.render_to_response({'form': form})


class FolderDetailsView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'folders/folder-details.html'
    context_object_name = 'projects'
    paginate_by = 6

    def get_queryset(self):
        folder = get_object_or_404(Folder, pk=self.kwargs['pk'], user=self.request.user)
        return folder.projects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        folder = get_object_or_404(Folder, pk=self.kwargs['pk'], user=self.request.user)
        context['folder'] = folder

        profile_user = folder.user.profile
        context['profile'] = profile_user

        context['is_own_profile'] = self.request.user == profile_user.user

        num_projects = context['projects'].count()
        context['empty_slots'] = max(self.paginate_by - num_projects, 0)

        return context


def remove_project_from_folder(request, pk, project_id):

    folder = get_object_or_404(Folder, id=pk, user=request.user)
    project = get_object_or_404(Project, id=project_id)

    if project in folder.projects.all():
        folder.projects.remove(project)

    return redirect('folder-details', pk=folder.id)