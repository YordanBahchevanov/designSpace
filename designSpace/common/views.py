from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, TemplateView
from designSpace.projects.models import Project


class HomePageView(ListView):
    model = Project
    template_name = 'common/home.html'
    context_object_name = 'projects'
    paginate_by = 3

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            projects = context['object_list']
            data = {
                'projects': [
                    {
                        'title': project.title,
                        'location': project.location,
                        'area': project.area,
                        'year': project.year,
                        'cover_image': project.cover_image.url,
                        'creator': {
                            'username': project.creator.username,
                            'display_name': project.creator.profile.full_name or project.creator.username,
                            'profile_picture': project.creator.profile.profile_picture.url if project.creator.profile.profile_picture else None,
                        },
                        'id': project.id,
                        'images': [
                            image.image.url for image in project.images.all()
                        ]
                    }
                    for project in projects
                ],
                'has_next': context['page_obj'].has_next()
            }
            return JsonResponse(data)

        return super().render_to_response(context, **response_kwargs)


class AboutView(TemplateView):
    template_name = 'common/about.html'


class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        if query:
            projects = Project.objects.filter(
                Q(title__icontains=query) |
                Q(location__icontains=query) |
                Q(creator__username__icontains=query)
            ).distinct()
        else:
            projects = Project.objects.none()

        data = {
            'projects': [
                {
                    'title': project.title,
                    'location': project.location,
                    'area': project.area,
                    'year': project.year,
                    'cover_image': project.cover_image.url,
                    'creator': {
                        'username': project.creator.username,
                        'display_name': project.creator.profile.full_name or project.creator.username,
                        'profile_picture': project.creator.profile.profile_picture.url if project.creator.profile.profile_picture else None,
                    },
                    'id': project.id,
                    'images': [
                        image.image.url for image in project.images.all()
                    ]
                }
                for project in projects
            ]
        }
        return JsonResponse(data)