from django.contrib import admin
from django.urls import include, path
from kanban_app.api.views import ContactView, ContactSingleView, TasksView,TaskSingleView ,UsersOfTaskList,SubatasksView,SubtaskSingleView
from rest_framework import routers


# API URL configuration for the Kanban app.
# Each path maps a URL to a class-based view handling CRUD operations.

urlpatterns = [
    # Contact endpoints
    path('contacts/', ContactView.as_view(), name='contact-list'),  # List and create contacts
    path('contacts/<int:pk>/', ContactSingleView.as_view(), name='contact-detail'),  # Retrieve, update, delete a single contact

    # Task endpoints
    path('tasks/', TasksView.as_view(), name='task-list'),  # List and create tasks
    path('tasks/<int:pk>/', TaskSingleView.as_view(), name='task-detail'),  # Retrieve, update, delete a single task

    # Get all users (contacts) assigned to a specific task
    path('tasks/<int:pk>/contacts/', UsersOfTaskList.as_view(), name='task-users'),

    # Subtask endpoints
    path('subtasks/', SubatasksView.as_view(), name='subtask-list'),  # List and create subtasks
    path('subtasks/<int:pk>/', SubtaskSingleView.as_view(), name='subtask-detail'),  # Retrieve, update, delete a subtask
]