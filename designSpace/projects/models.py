from datetime import datetime

from cloudinary.api import delete_resources_by_prefix, delete_folder, resources
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from designSpace.projects.choices import ProjectTypeChoice
from designSpace.projects.utils import get_cover_image_folder, get_gallery_image_folder

UserModel = get_user_model()

class Project(models.Model):
    creator = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    title = models.CharField(
        max_length=100,
    )

    project_type = models.CharField(
        max_length=20,
        choices=ProjectTypeChoice.choices,
        default=ProjectTypeChoice.OTHER,
    )

    year = models.PositiveIntegerField()

    area = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text = "Area in square meters",
    )

    location = models.CharField(
        max_length=100,
    )

    cover_image = CloudinaryField('image', folder=get_cover_image_folder)

    cover_image_public_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def user_likes(self, user):
        """Check if the user has liked this project"""
        return self.likes.filter(user=user).exists()

    def clean(self):
        super().clean()

        if not self.project_type:
            raise ValidationError("Project type is required.")

        current_year = datetime.now().year

        if self.year and (self.year < 1900 or self.year > current_year):
            raise ValidationError(f"Year must be between 1900 and {current_year}.")

    def delete(self, *args, **kwargs):
        folder_path = get_cover_image_folder(self)

        try:
            delete_resources_by_prefix(folder_path)

            delete_folder(folder_path)
        except Exception as e:
            print(f"Error while deleting Cloudinary resources or folder: {e}")

        super().delete(*args, **kwargs)


class ProjectImage(models.Model):
    project = models.ForeignKey(
        to=Project,
        related_name='images',
        on_delete=models.CASCADE,
    )

    image = CloudinaryField(
        'image',
        folder=get_gallery_image_folder,
        blank=True,
        null=True
    )

    image_public_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Image for {self.project.title}"
