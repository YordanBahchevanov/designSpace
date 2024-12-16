from django.contrib.auth import get_user_model
from django.db import models


UserModel = get_user_model()

class Article(models.Model):
    author = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name="articles"
    )

    title = models.CharField(
        max_length=100
    )

    content = models.TextField(
        max_length=5000
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    class Meta:
        ordering = ['-created_at']
