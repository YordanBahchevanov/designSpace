from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from designSpace.projects.models import Project

UserModel = get_user_model()

class Folder(models.Model):
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name='folders'
    )

    projects = models.ManyToManyField(
        to=Project,
        related_name='folders_in',
        blank=True
    )

    title = models.CharField(
        max_length=30
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('folder-details', args=[str(self.slug)])

    class Meta:
        ordering = ['-created_at']
