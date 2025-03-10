from django.contrib import admin
from django.urls import include, path
from kanban_app.api.views import ContactView, ContactSingleView, TasksView,TaskSingleView ,UsersOfTaskList,SubatasksView,SubtaskSingleView
from rest_framework import routers


urlpatterns = [
    path('contacts/', ContactView.as_view(), name='contact-list'),
    path('contacts/<int:pk>/', ContactSingleView.as_view(), name ='contact-detail'),
    path('tasks/', TasksView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskSingleView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/contacts/', UsersOfTaskList.as_view()),
    path('subtasks/', SubatasksView.as_view(), name='subtask-list'),
    path('subtasks/<int:pk>/', SubtaskSingleView.as_view(), name='subtask-detail')
]