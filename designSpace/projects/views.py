import logging

from cloudinary.uploader import upload, destroy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .forms import ProjectCreateForm, ProjectImageFormSet, ProjectEditForm
from .models import Project, ProjectImage
from .permissions import IsProjectOwner
from .serializers import ProjectSerializer
from .utils import get_cover_image_folder, get_gallery_image_folder
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

        context['user_pk'] = self.request.user.pk

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

logger = logging.getLogger('designSpace')

class ProjectEditView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectEditForm
    template_name = "projects/project-edit.html"
    login_url = reverse_lazy("log-in")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_pk"] = self.request.user.pk

        # Populate image_formset with the existing images for the project
        if self.request.POST:
            context["image_formset"] = ProjectImageFormSet(
                self.request.POST, self.request.FILES, queryset=self.get_object().images.all()
            )
        else:
            context["image_formset"] = ProjectImageFormSet(queryset=self.get_object().images.all())

        return context

    def form_valid(self, form):
        project = form.save(commit=False)

        # Handle cover image upload and deletion
        old_cover_image_public_id = project.cover_image_public_id
        new_cover_image = form.cleaned_data.get("cover_image")

        if new_cover_image and hasattr(new_cover_image, "read"):
            upload_response = upload(
                new_cover_image,
                folder=get_cover_image_folder(project)
            )

            if old_cover_image_public_id:
                try:
                    destroy(old_cover_image_public_id)
                except Exception as e:
                    messages.error(self.request, f"Error deleting old cover image: {e}")

            project.cover_image = upload_response["secure_url"]
            project.cover_image_public_id = upload_response["public_id"]

        project.save()

        # Handle gallery images (upload new or delete)
        image_formset = ProjectImageFormSet(
            self.request.POST,
            self.request.FILES,
            queryset=project.images.all(),
        )

        logger.debug(f"Image Formset is valid: {image_formset.is_valid()}")
        logger.debug(f"Formset cleaned data: {image_formset.cleaned_data}")

        if image_formset.is_valid():
            for image_form in image_formset:
                logger.debug(f"Processing image form: {image_form.cleaned_data}")

                # Check if the DELETE checkbox is checked
                if image_form.cleaned_data.get("DELETE"):
                    logger.debug(f"Deleting image: {image_form.instance}")
                    # Delete image from Cloudinary and remove from database
                    if image_form.instance.image_public_id:
                        try:
                            destroy(image_form.instance.image_public_id)
                        except Exception as e:
                            messages.error(self.request, f"Error deleting image: {e}")
                    image_form.instance.delete()  # Delete image instance

                # If a new image is uploaded, upload to Cloudinary and save
                elif image_form.cleaned_data.get("image"):
                    logger.debug(f"Uploading new image: {image_form.cleaned_data.get('image')}")
                    new_image = image_form.cleaned_data.get("image")
                    if hasattr(new_image, "read"):
                        upload_response = upload(new_image, folder=get_gallery_image_folder(project))
                        image_form.instance.image = upload_response["secure_url"]
                        image_form.instance.image_public_id = upload_response["public_id"]

                    # Ensure the image is linked to the project
                    image_form.instance.project = project
                    image_form.save()

        else:
            logger.debug(f"Formset errors: {image_formset.errors}")
            messages.error(self.request, "There were errors with the image formset.")

        # Display a success message
        messages.success(self.request, "Your project has been updated successfully.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("projects:project-details", kwargs={"slug": self.object.slug})

    def get_login_url(self):
        return f"{reverse_lazy('log-in')}?next={self.request.path}"


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "projects/project-delete.html"
    success_url = reverse_lazy("profile-details")

    def get_object(self, queryset=None):
        return get_object_or_404(
            Project,
            slug=self.kwargs['slug'],
            creator=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = getattr(self.request.user, 'profile', None)

        return context

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={
                'pk': self.request.user.pk,
            }
        )

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Your project has been deleted successfully.")

        return super().delete(request, *args, **kwargs)



