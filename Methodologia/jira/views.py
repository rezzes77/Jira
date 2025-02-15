from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from .models import Developer, Project, Task
from .forms import DeveloperForm, ProjectForm, TaskForm


# Главная страница со списком задач
def task_list(request):
    tasks = Task.objects.all()

    # Фильтрация задач
    filters = {
        "status": request.GET.get("status"),
        "title__icontains": request.GET.get("q"),
        "developer__id": request.GET.get("developer"),
        "deadline": request.GET.get("date"),
    }

    # Применяем фильтры
    tasks = tasks.filter(**{k: v for k, v in filters.items() if v})

    context = {
        'tasks': tasks,
        'developers': Developer.objects.all(),
    }
    return render(request, 'task_list.html', context)


# Список разработчиков
def developer_list(request):
    context = {
        'developers': Developer.objects.all()
    }
    return render(request, 'developer_list.html', context)


# Список проектов
def project_list(request):
    context = {
        'projects': Project.objects.all()
    }
    return render(request, 'project_list.html', context)


# Добавление разработчика
def add_developer(request):
    if request.method == 'POST':
        form = DeveloperForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('developer_list')
    else:
        form = DeveloperForm()
    return render(request, 'add_developer.html', {'form': form})


# Добавление проекта
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'add_project.html', {'form': form})


# Добавление задачи
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})


# Редактирование задачи
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form})


# Удаление задачи
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'delete_task.html', {'task': task})\



def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')  # Перенаправление на страницу со списком проектов
    else:
        form = ProjectForm(instance=project)
    return render(request, 'edit_project.html', {'form': form})

# Удаление проекта
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')  # Перенаправление на страницу со списком проектов
    return render(request, 'delete_project.html', {'project': project})


# Изменение разработчика
def edit_developer(request, pk):
    developer = get_object_or_404(Developer, pk=pk)
    if request.method == 'POST':
        form = DeveloperForm(request.POST, instance=developer)
        if form.is_valid():
            form.save()
            return redirect('developer_list')  # Перенаправление на страницу со списком разработчиков
    else:
        form = DeveloperForm(instance=developer)
    return render(request, 'edit_developer.html', {'form': form})

# Удаление разработчика
def delete_developer(request, pk):
    developer = get_object_or_404(Developer, pk=pk)
    if request.method == 'POST':
        developer.delete()
        return redirect('developer_list')  # Перенаправление на страницу со списком разработчиков
    return render(request, 'delete_developer.html', {'developer': developer})

# Перемещение задачи между статусами (AJAX)
@require_POST
def move_task(request, pk, status):
    task = get_object_or_404(Task, pk=pk)
    if status not in ["todo", "in_progress", "done"]:
        return JsonResponse({'error': 'Некорректный статус'}, status=400)

    task.status = status
    task.save()
    return JsonResponse({'success': True})