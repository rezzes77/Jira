import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    developer__name = django_filters.CharFilter(lookup_expr='icontains')
    project__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Task
        fields = ['title', 'developer__name', 'project__name', 'status', 'priority']