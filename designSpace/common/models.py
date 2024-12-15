from django.contrib.auth import get_user_model
from django.db import models

from designSpace.projects.models import Project

UserModel = get_user_model()

class Like(models.Model):
    to_project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='liked_projects',
    )

    class Meta:
        unique_together = ('to_project', 'user')

    def __str__(self):
        return f"{self.user.username} likes {self.to_project.title}"
