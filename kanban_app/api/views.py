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
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAdminForDeleteOrPatchOrReadOnly]

    

class ContactSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsOwner]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"contact": serializer.data,"message": "Contact successfully updated", }, status= status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message':'Contact succesfully deleted'}, status= status.HTTP_200_OK)
    
    
class UsersOfTaskList(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        task = Task.objects.get(pk=pk)
        return task.contacts.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        task = Task.objects.get(pk=pk)
        user = serializer.save()
        task.contacts.add(user)
        task.save()
        
class TasksView(generics.ListCreateAPIView):
    queryset = Task.objects.all();
    serializer_class = TaskSerializer;
    permission_classes = [IsStaffOrReadOnly]
    
    
class TaskSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsStaffOrReadOnly]
    

class SubatasksView(generics.ListCreateAPIView):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    permission_classes = [IsStaffOrReadOnly]
    
    
class SubtaskSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    permission_classes = [IsStaffOrReadOnly]
     