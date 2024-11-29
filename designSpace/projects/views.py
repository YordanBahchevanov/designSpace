from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from designSpace.projects.forms import ProjectCreateForm, ProjectImageFormSet
from designSpace.projects.models import Project, ProjectImage


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = "projects/create-project.html"
    success_url = reverse_lazy("home")

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