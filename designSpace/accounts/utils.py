def get_profile_image_folder(instance):
    """Generate folder path for the profile image."""
    return f"users/{instance.user.username}/profile-image/"
