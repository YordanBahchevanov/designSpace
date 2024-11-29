from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Project

@receiver(pre_save, sender=Project)
def generate_project_slug(sender, instance, **kwargs):
    """
    Generate a unique slug for the Project model before saving.
    """
    if not instance.slug:
        base_slug = slugify(instance.title)
        slug = base_slug
        count = 1

        while Project.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1

        instance.slug = slug