from django.contrib import admin
from django.urls import include, path
from kanban_app.api.views import ContactView, ContactSingleView, tasks_view,task_single_view ,UsersOfTaskList,SubtaskViewSet, subtask_view, subtask_single_view
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'subtasks', SubtaskViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('contacts/', ContactView.as_view(), name='contact-list'),
    path('contacts/<int:pk>', ContactSingleView.as_view(), name ='contact-detail'),
    path('tasks/', tasks_view),
    path('tasks/<int:pk>/', task_single_view, name='task-detail'),
    path('tasks/<int:pk>/users/', UsersOfTaskList.as_view()),
    path('subtasks/', subtask_view),
    path('subtasks/<int:pk>', subtask_single_view)
]