from django.shortcuts import render
from django.views.generic import ListView


# class HomePage(ListView):
#     model = Photo
#     template_name = 'common/home-page.html'
#     context_object_name = 'all_photos'  # by default is object_list and photos
#     paginate_by = 10
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         context['comment_form'] = CommentForm()
#         context['search_form'] = SearchForm(self.request.GET)
#
#         user = self.request.user
#
#         for photo in context['all_photos']:
#             photo.has_liked = photo.like_set.filter(user=user).exists() if user.is_authenticated else False
#
#         return context
#
#     def get_queryset(self):
#         queryset = super().get_queryset()  # All objects
#         pet_name = self.request.GET.get('pet_name')
#
#         if pet_name:
#             queryset = queryset.filter(  # Filter the objects
#                 tagged_pets__name__icontains=pet_name
#             )
#
#         return queryset  # Return the new queryset
