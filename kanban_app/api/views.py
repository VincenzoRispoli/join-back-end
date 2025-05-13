from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from kanban_app.models import Contact, Subtask, Task
from kanban_app.api.serializers import ContactSerializer, TaskSerializer, SubtaskSerializer
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsAdminForDeleteOrPatchOrReadOnly, IsOwner, IsStaffOrReadOnly


class ContactView(APIView):
    """
    API endpoint to list all contacts or create a new contact.
    Accessible only to staff and superusers for write operations.
    """
    permission_classes = [IsAdminForDeleteOrPatchOrReadOnly]

    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        print(request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            print(f"{serializer.data}")
            return Response({'data': serializer.data, 'ok': True, 'message': 'Contact successfully created'})
        else:
            return Response({'data': serializer.errors, 'ok': False, 'error': 'Contact not created, an error occurred'})


class ContactSingleView(APIView):
    """
    API endpoint to retrieve, update or delete a specific contact.
    Only the owner, superuser, or 'Guest' can perform non-safe operations.
    """
    permission_classes = [IsOwner]

    def get(self, request, pk):
        contact = Contact.objects.get(pk=pk)
        serializer = ContactSerializer(contact)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        contact = Contact.objects.get(pk=pk)
        serializer = ContactSerializer(
            contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'ok': True, 'message': 'Contact successfully updated'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'data': serializer.errors, 'ok': False, 'error': 'Error while updating the contact'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contact = Contact.objects.get(pk=pk)
        serializer = ContactSerializer(contact)
        contact.delete()
        return Response({'data': serializer.data, 'message': 'Contact successfully deleted'}, status=status.HTTP_200_OK)


class UsersOfTaskList(generics.ListCreateAPIView):
    """
    API endpoint to list or assign users (contacts) to a specific task.
    - GET: lists users assigned to a task.
    - POST: adds a contact to the task.
    """
    serializer_class = ContactSerializer

    def get_queryset(self):
        """
        Return the list of contacts associated with a specific task.
        """
        pk = self.kwargs.get('pk')
        task = get_object_or_404(Task, pk=pk)
        return task.contacts.all()

    def perform_create(self, serializer):
        """
        Assign a new contact to the task.
        """
        pk = self.kwargs.get('pk')
        task = get_object_or_404(Task, pk=pk)
        user = serializer.save()
        task.contacts.add(user)
        task.save()


# -------------------------
# TASK VIEWS
# -------------------------

class TaskListView(APIView):
    """
    API endpoint to list or create tasks.
    Write operations are restricted to staff users.
    """
    # permission_classes = [IsStaffOrReadOnly]

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'ok': True, 'message': 'Task successfully created'})
        else:
            return Response({'data': serializer.errors, 'ok': False, 'error': 'Task not created, an error occurred'})


class TaskDetailView(APIView):
    """
    API endpoint to retrieve, update or delete a single task.
    Write and delete operations require staff permissions.
    """
    permission_classes = [IsStaffOrReadOnly]

    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'ok': True, 'message': 'Task successfully updated'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'data': serializer.errors, 'ok': False, 'error': 'An error occurred during Task updating'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.delete()
        return Response({'ok': True, 'message': 'Task successfully deleted'})


# -------------------------
# SUBTASK VIEWS
# -------------------------

class SubatasksListView(APIView):
    """
    API endpoint to list all subtasks or create a new subtask.
    Write access is limited to staff users.
    """
    permission_classes = [IsStaffOrReadOnly]

    def get(self, request):
        subtasks = Subtask.objects.all()
        serializer = SubtaskSerializer(subtasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubtaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'ok': True, 'message': 'Subtask successfully created'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'data': serializer.errors, 'ok': False, 'error': 'An error  occurred during the subtask creation'}, status=status.HTTP_400_BAD_REQUEST)


class SubtaskSingleView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a single subtask.
    Only staff users have write/delete access.
    """
    permission_classes = [IsStaffOrReadOnly]

    def get(self, request, pk):
        subtask = Subtask.objects.get(pk=pk)
        serializer = SubtaskSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        subtask = Subtask.objects.get(pk=pk)
        serializer = SubtaskSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'ok': True, 'message': 'Subtask successfully updated'})
        else:
            return Response({'data': serializer.errors, 'ok': False, 'error': 'An error occurred during subtask updating'})

    def delete(self, request, pk):
        subtask = Subtask.objects.get(pk=pk)
        serializer = SubtaskSerializer(subtask)
        subtask.delete()
        return Response({'data': serializer.data, 'ok': True, 'message': 'Subtask successfully deleted'})
