from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, TemplateView

from designSpace.articles.models import Article
from designSpace.common.models import Like
from designSpace.common.utils import serialize_project
from designSpace.projects.models import Project


def custom_404_view(request, exception):
    return render(request, 'common/404.html', {}, status=404)


# class HomePageView(ListView):
#     model = Project
#     template_name = 'common/home.html'
#     context_object_name = 'projects'
#     paginate_by = 3
#
#     def render_to_response(self, context, **response_kwargs):
#         if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             projects = context['object_list']
#             data = {
#                 'projects': [serialize_project(project) for project in projects],
#                 'has_next': context['page_obj'].has_next(),
#             }
#             return JsonResponse(data)
#
#         return super().render_to_response(context, **response_kwargs)


class HomePageView(ListView):
    model = Project
    template_name = 'common/home.html'
    context_object_name = 'projects'
    paginate_by = 3

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_likes = Like.objects.filter(user=self.request.user)
            return Project.objects.prefetch_related(
                Prefetch('likes', queryset=user_likes, to_attr='user_likes')
            )
        else:
            return Project.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        latest_articles = Article.objects.all().order_by('-created_at')[:5]
        context['articles'] = latest_articles

        return context


class AboutView(TemplateView):
    template_name = 'common/about.html'


class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        if query:
            search_query = SearchQuery(query)

            projects = Project.objects.annotate(
                search=SearchVector(
                    'title',
                    'location',
                    'creator__username',
                    'creator__profile__first_name',
                    'creator__profile__last_name',
                ),

                search_rank=SearchRank(
                    SearchVector('title',
                                 'creator__username',
                                 'creator__profile__first_name',
                                 'creator__profile__last_name',
                                 'location',
                                 ),
                    search_query
                )
            ).filter(
                Q(search=search_query) |
                Q(title__icontains=query) |
                Q(location__icontains=query) |
                Q(creator__username__icontains=query) |
                Q(creator__profile__first_name__icontains=query) |
                Q(creator__profile__last_name__icontains=query)
            ).distinct().order_by('-search_rank')

        else:
            projects = Project.objects.none()

        data = {
            'projects': [serialize_project(project) for project in projects]
        }
        return JsonResponse(data)


@login_required
def like_project(request, project_id):
    if request.method == "GET":
        project = get_object_or_404(Project, id=project_id)
        like, created = Like.objects.get_or_create(to_project=project, user=request.user)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        return JsonResponse({
            "liked": liked,
            "like_count": project.likes.count(),
        })
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)



# @login_required
# def like_project(request, project_id: int):
#     project = get_object_or_404(Project, id=project_id)
#
#     liked_object = Like.objects.filter(to_project=project, user=request.user).first()
#
#     if liked_object:
#         liked_object.delete()
#         liked = False
#     else:
#         Like.objects.create(to_project=project, user=request.user)
#         liked = True
#
#     return JsonResponse({
#         'liked': liked,
#         'like_count': project.likes.count(),
#     })