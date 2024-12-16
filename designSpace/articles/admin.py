from django.contrib import admin

from designSpace.articles.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'content', 'created_at')
    search_fields = ('title', 'author__username',)
    list_filter = ('author', 'created_at')

    def has_add_permission(self, request):
        if request.user.groups.filter(name='Writer').exists():
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='Writer').exists():
            return True
        return super().has_change_permission(request, obj=obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='Writer').exists():
            return True
        return super().has_delete_permission(request, obj=obj)


