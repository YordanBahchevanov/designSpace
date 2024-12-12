from cloudinary.uploader import upload
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .forms import ProjectCreateForm, ProjectImageFormSet
from .models import Project, ProjectImage
from .permissions import IsProjectOwner
from .serializers import ProjectSerializer
from ..accounts.models import Profile


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectOwner]


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
        return get_object_or_404(Project, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = self.get_object()

        profile_user = get_object_or_404(Profile, user=project.creator)
        context['profile'] = profile_user

        context['is_creator'] = self.request.user == project.creator

        return context



