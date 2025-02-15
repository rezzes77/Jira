# forms.py
from django import forms
from .models import Developer, Project, Task

class DeveloperForm(forms.ModelForm):
    class Meta:
        model = Developer
        fields = ['name', 'email', 'group', 'number']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'developers', 'description', 'deadline']
        widgets = {
            'developers': forms.CheckboxSelectMultiple(),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'developer', 'project', 'deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }