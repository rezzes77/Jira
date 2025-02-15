from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from .models import Developer, Project, Task
from .forms import DeveloperForm, ProjectForm, TaskForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    if 'guest' in request.session:
        del request.session['guest']
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')
        else:
            return render(request, 'login.html', {'error': 'Неверные данные'})
    return render(request, 'login.html')

@require_http_methods(["GET"])
def guest_access(request):
    request.session['guest'] = True
    return redirect('task_list')



def check_guest(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('guest'):
            return HttpResponseForbidden("Доступ запрещен для гостей")
        return view_func(request, *args, **kwargs)
    return wrapper

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

    # Группируем задачи по статусам
    tasks_by_status = {
        'todo': tasks.filter(status='todo'),
        'in_progress': tasks.filter(status='in_progress'),
        'done': tasks.filter(status='done'),
    }

    context = {
        'tasks_by_status': tasks_by_status,
        'developers': Developer.objects.all(),
    }
    return render(request, 'task_list.html', context)


# Перемещение задачи между статусами
@login_required
@require_POST
def move_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    next_status = request.POST.get('next_status')

    if next_status in ['todo', 'in_progress', 'done']:
        task.status = next_status
        task.save()

    return redirect('task_list')  # Перенаправляем обратно на список задач

def info_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'info_task.html', {'task': task})


@login_required
# Список разработчиков
def developer_list(request):
    context = {
        'developers': Developer.objects.all()
    }
    return render(request, 'developer_list.html', context)

@login_required
# Список проектов
def project_list(request):
    context = {
        'projects': Project.objects.all()
    }
    return render(request, 'project_list.html', context)

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
# Удаление задачи
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'delete_task.html', {'task': task})\


@login_required
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

@login_required
# Удаление проекта
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')  # Перенаправление на страницу со списком проектов
    return render(request, 'delete_project.html', {'project': project})


@login_required
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

@login_required
# Удаление разработчика
def delete_developer(request, pk):
    developer = get_object_or_404(Developer, pk=pk)
    if request.method == 'POST':
        developer.delete()
        return redirect('developer_list')  # Перенаправление на страницу со списком разработчиков
    return render(request, 'delete_developer.html', {'developer': developer})

