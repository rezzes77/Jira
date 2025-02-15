from django.contrib import admin
from .models import Developer, Project, Task

@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'group', 'number')
    search_fields = ('name', 'email', 'group', 'number')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'deadline')
    search_fields = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'developer', 'status', 'priority', 'project', 'deadline')
    list_filter = ('status', 'priority', 'developer', 'project')
    search_fields = ('title', 'developer__name', 'project__name')
