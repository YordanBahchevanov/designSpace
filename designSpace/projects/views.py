from cloudinary.uploader import upload
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .forms import ProjectCreateForm, ProjectImageFormSet
from .models import Project, ProjectImage
from .serializers import ProjectSerializer
from ..accounts.models import Profile


class ListProjectView(ListCreateAPIView):
    projects = Project.objects.prefetch_related('images').select_related('creator')
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = "projects/create-project.html"
    success_url = reverse_lazy("home")
    login_url = reverse_lazy('log-in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["image_formset"] = ProjectImageFormSet(self.request.POST, self.request.FILES)
        else:
            context["image_formset"] = ProjectImageFormSet(queryset=ProjectImage.objects.none())
        return context

    def form_valid(self, form):
        project = form.save(commit=False)
        project.creator = self.request.user
        project.save()

        image_formset = ProjectImageFormSet(self.request.POST, self.request.FILES)

        if image_formset.is_valid():
            for image_form in image_formset:
                if image_form.cleaned_data.get("image"):
                    ProjectImage.objects.create(project=project, image=image_form.cleaned_data["image"])

        return redirect(self.success_url)

    def get_login_url(self):
        return f"{reverse_lazy('log-in')}?next={self.request.path}"


class ProjectDetailsView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    context_object_name = 'project'

    def get_object(self, queryset=None):
        # Retrieve project by slug
        return get_object_or_404(Project, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = self.get_object()

        # Fetch profile based on the creator of the project
        profile_user = get_object_or_404(Profile, user=project.creator)
        context['profile'] = profile_user

        # Determine if the current user is the project creator
        context['is_creator'] = self.request.user == project.creator

        # Calculate the number of images (accounting for cover image and gallery)
        num_images = project.images.count()

        # Assume 6 is the max slot for images
        context['empty_slots'] = max(6 - num_images, 0)

        return context



