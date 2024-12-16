from rest_framework.permissions import BasePermission


class IsArticleOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        article_author = obj.author.username

        return request.user.username in article_author

