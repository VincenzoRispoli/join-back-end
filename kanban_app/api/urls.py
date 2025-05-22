from django.contrib import admin
from django.urls import include, path
from kanban_app.api.views import ContactView, ContactSingleView, TaskListView, TaskDetailView, SubatasksListView, SubtaskSingleView


# API URL configuration for the Kanban app.
# Each path maps a URL to a class-based view handling CRUD operations.

urlpatterns = [
    # Contact endpoints
    path('contacts/', ContactView.as_view(), name='contact-list'),  # List and create contacts
    # Retrieve, update, delete a single contact
    path('contacts/<int:pk>/', ContactSingleView.as_view(), name='contact-detail'),

    # Task endpoints
    path('tasks/', TaskListView.as_view(), name='task-list'),  # List and create tasks
    # Retrieve, update, delete a single task
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

    # Subtask endpoints
    path('subtasks/', SubatasksListView.as_view(), name='subtask-list'),  # List and create subtasks
    path('subtasks/<int:pk>/', SubtaskSingleView.as_view(), name='subtask-detail'),  # Retrieve, update, delete a subtask
]
