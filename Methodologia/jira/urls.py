from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.task_list, name='task_list'),

    # Разработчики
    path('developers/', views.developer_list, name='developer_list'),
    path('add-developer/', views.add_developer, name='add_developer'),

    # Проекты
    path('projects/', views.project_list, name='project_list'),
    path('add-project/', views.add_project, name='add_project'),

    # Задачи
    path('add-task/', views.add_task, name='add_task'),
    path('edit-task/<int:pk>/', views.edit_task, name='edit_task'),
    path('delete-task/<int:pk>/', views.delete_task, name='delete_task'),

    # AJAX
    path('move_task/<int:pk>/', views.move_task, name='move_task'),

    path('edit_project/<int:pk>/', views.edit_project, name='edit_project'),
    path('delete_project/<int:pk>/', views.delete_project, name='delete_project'),
    path('task/<int:task_id>/', views.info_task, name='info_task'),

    path('edit_developer/<int:pk>/', views.edit_developer, name='edit_developer'),
    path('delete_developer/<int:pk>/', views.delete_developer, name='delete_developer'),
    path('login/', views.login_view, name='login'),
    path('guest/', views.guest_access, name='guest_access'),
    path('logout/', views.custom_logout, name='logout'),

]

