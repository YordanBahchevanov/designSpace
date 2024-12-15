from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Article

@receiver(pre_save, sender=Article)
def generate_article_slug(sender, instance, **kwargs):
    """
    Generate a unique slug for the Project model before saving.
    """
    if not instance.slug:
        base_slug = slugify(instance.title)
        slug = base_slug
        count = 1

        while Article.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1

        instance.slug = slug