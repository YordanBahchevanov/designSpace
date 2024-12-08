from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView

from designSpace.common.utils import serialize_project
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
                'projects': [serialize_project(project) for project in projects],
                'has_next': context['page_obj'].has_next(),
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
                # Q(creator__full_name__icontains=query)
            ).distinct()
        else:
            projects = Project.objects.none()

        data = {
            'projects': [serialize_project(project) for project in projects]
        }
        return JsonResponse(data)


# @login_required
# def likes_functionality(request, photo_id: int):
#     liked_object = Like.objects.filter(
#         to_project_id=project_pk,
#         user=request.user
#     ).first()
#
#     if liked_object:
#         liked_object.delete()
#     else:
#         like = Like(to_photo_id=photo_id, user=request.user)
#         like.save()
#
#     return redirect(request.META.get('HTTP_REFERER') + f'#{photo_id}')