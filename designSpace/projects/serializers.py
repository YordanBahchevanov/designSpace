from rest_framework import serializers
from .models import Project, ProjectImage
from ..accounts.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'profile_picture', 'display_name']

    def get_display_name(self, obj):
        return obj.full_name or obj.user.username


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'project']


class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    creator = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'creator',
            'title',
            'project_type',
            'year',
            'area',
            'location',
            'cover_image',
            'description',
            'created_at',
            'slug',
            'images'
        ]

    def get_creator(self, obj):
        profile = obj.creator.profile
        return {
            'username': obj.creator.username,
            'display_name': profile.full_name or obj.creator.username,
            'profile_picture': profile.profile_picture.url if profile.profile_picture else None,
        }

