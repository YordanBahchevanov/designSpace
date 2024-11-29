from django.contrib import admin

from designSpace.projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'location', 'project_type')
    search_fields = ('title', 'location', 'creator__username', 'project_type')
    list_filter = ('project_type', 'created_at')



