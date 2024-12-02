def get_cover_image_folder(instance):
    """Generate folder path for the cover image."""
    return f"users/{instance.creator.username}/projects/{instance.slug}/"

def get_gallery_image_folder(instance):
    """Generate folder path for gallery images."""
    return f"users/{instance.project.creator.username}/projects/{instance.project.slug}/gallery/"

