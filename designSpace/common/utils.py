from django.urls import reverse


def serialize_project(project):

    return {
        'title': project.title,
        'location': project.location,
        'area': project.area,
        'year': project.year,
        'cover_image': project.cover_image.url,
        'creator': {
            'username': project.creator.username,
            'display_name': project.creator.profile.full_name or project.creator.username,
            'profile_picture': project.creator.profile.profile_picture.url if project.creator.profile.profile_picture else None,
            'profile_url': reverse('profile-details', args=[project.creator.id]),
        },
        'id': project.id,
        'slug': project.slug,
        # 'like_url': reverse('like-project', kwargs={'slug': project.slug}),
        # 'like_count': project.likes.count,
        'project_url': reverse('projects:project-details', args=[project.slug]),
        'images': [
            image.image.url for image in project.images.all()
        ]
    }