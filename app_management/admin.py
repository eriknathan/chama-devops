from django.contrib import admin
from .models import Project, Topic

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin para Projetos."""
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Admin para Tópicos."""
    list_display = ('name', 'created_at')
    search_fields = ('name',)
