from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from kanban_app.models import Contact, Subtask, User, Task
from kanban_app.api.serializers import ContactSerializer, TaskHyperLinkedSerializer, TaskSerializer, SubtaskSerializer
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsAdminForDeleteOrPatchOrReadOnly, IsOwner, IsStaffOrReadOnly 

class ContactView(generics.ListCreateAPIView):
    """
    API endpoint to list all contacts or create a new contact.
    Accessible only to staff and superusers for write operations.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAdminForDeleteOrPatchOrReadOnly]


class ContactSingleView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update or delete a specific contact.
    Only the owner, superuser, or 'Guest' can perform non-safe operations.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsOwner]

    def update(self, request, *args, **kwargs):
        """
        Partially update a contact instance.
        Returns a custom response with a success message.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "contact": serializer.data,
                "message": "Contact successfully updated"
            }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a contact and return a confirmation message.
        """
        super().destroy(request, *args, **kwargs)
        return Response({'message': 'Contact successfully deleted'}, status=status.HTTP_200_OK)


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

class TasksView(generics.ListCreateAPIView):
    """
    API endpoint to list or create tasks.
    Write operations are restricted to staff users.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsStaffOrReadOnly]


class TaskSingleView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update or delete a single task.
    Write and delete operations require staff permissions.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsStaffOrReadOnly]


# -------------------------
# SUBTASK VIEWS
# -------------------------

class SubatasksView(generics.ListCreateAPIView):
    """
    API endpoint to list all subtasks or create a new subtask.
    Write access is limited to staff users.
    """
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    permission_classes = [IsStaffOrReadOnly]


class SubtaskSingleView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a single subtask.
    Only staff users have write/delete access.
    """
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    permission_classes = [IsStaffOrReadOnly]
     