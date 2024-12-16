from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'

    def get_author(self, obj):
        profile = obj.author.profile
        return {
            'username': obj.author.username,
            'display_name': profile.full_name or obj.author.username,
        }