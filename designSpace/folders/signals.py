from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Folder

@receiver(pre_save, sender=Folder)
def generate_folder_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)
        slug = base_slug
        count = 1

        while Folder.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1

        instance.slug = slug