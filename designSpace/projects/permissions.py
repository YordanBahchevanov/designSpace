from rest_framework.permissions import BasePermission


class IsProjectOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        project_publisher = obj.creator.username

        return request.user.username in project_publisher

