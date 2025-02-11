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


# class UsersView(mixins.ListModelMixin,
#                 mixins.CreateModelMixin,
#                 generics.GenericAPIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class ContactView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAdminForDeleteOrPatchOrReadOnly]

    

class ContactSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsOwner]
    
    # def get(self, request, *args, **kwargs):
    #     return self.retrieve(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)
    


# @api_view(['GET', 'POST'])
# def users_view(request):
#     if request.method == 'GET':
#        users = User.objects.all();
#        serializer = UserSerializer(users, many=True, context={'request': request})
#        return Response(serializer.data)
#     if request.method == 'POST':
#         serializer = UserSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
# @api_view(['GET','DELETE', 'PUT'])
# def user_single_view(request, pk):
#     if request.method == 'GET':
#         user = User.objects.get(pk = pk)
#         serializer = UserSerializer(user, context={'request':request})
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         user = User.objects.get(pk = pk)
#         serializer = UserSerializer(user, data = request.data, partial = True)
#         if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
    
#     if request.method == 'DELETE':
#         user = User.objects.get(pk = pk)
#         serializer = UserSerializer(user)
#         user.delete()
#         return Response(serializer.data)


class UsersOfTaskList(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        task = Task.objects.get(pk=pk)
        return task.users.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        task = Task.objects.get(pk=pk)
        user = serializer.save()
        # serializer.save(task = [task])
        task.users.add(user)
        task.save()
        

    
@api_view(['GET', 'POST'])
def tasks_view(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many= True, context={'request':request})
        print(f"Get method {serializer.data}")
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = TaskSerializer(data = request.data, context={'request':request})
        print(f"request data {request.data}")
        if serializer.is_valid():
           task = serializer.save()
           if 'contacts_ids' in request.data:
               task.contacts.set(request.data['contacts_ids'])
               return Response(serializer.data)
        return Response(serializer.errors)

        
        
@api_view(['GET', 'DELETE', 'PUT'])
def task_single_view(request, pk):
     if request.method == 'GET':
         task = Task.objects.get(pk=pk)
         serializer = TaskSerializer(task, context={'request':request})
         return Response(serializer.data)
     
     if request.method == 'DELETE':
         task = Task.objects.get(pk=pk)
         serializer = TaskSerializer(task, context={'request':request})
         data = serializer.data
         task.delete()
         return Response(data)
     
     if request.method == 'PUT':
         task = Task.objects.get(pk=pk)
         serializer = TaskSerializer(task, data = request.data, partial=True, context={'request':request})
         if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
         else:
            return Response(serializer.errors)
        
    
class SubtaskViewSet(viewsets.ModelViewSet):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    
      
      
class SubtaskViewSetOld(viewsets.ViewSet):
    queryset = Subtask.objects.all()
    
    def list(self, request):
        serializer = SubtaskSerializer(self.queryset, many=True, context={'request': request} )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        subtask = get_object_or_404(self.queryset, pk=pk)
        serializer = SubtaskSerializer(subtask)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = SubtaskSerializer(data=request.data, many=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def destroy(self, request, pk=None):
        subtask = get_object_or_404(self.queryset, pk=pk)
        serializer = SubtaskSerializer(subtask)
        subtask.delete()
        return Response(serializer.data)





        
@api_view(['GET', 'POST'])
def subtask_view(request):
    if request.method == 'GET':
        subtasks = Subtask.objects.all()
        serializer = SubtaskSerializer(subtasks, many=True, context={'request': request})
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = SubtaskSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)


@api_view(['GET','PUT', 'DELETE'])
def subtask_single_view(request, pk):
    if request.method == 'GET':
        subtask = Subtask.objects.get(pk = pk)
        serializer = SubtaskSerializer(subtask, context={'request': request})
        print("the subtasks data are", serializer.data)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        subtask = Subtask.objects.get(pk=pk)
        serializer = SubtaskSerializer(subtask, data= request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
    if request.method == 'DELETE':
       subtask = Subtask.objects.get(pk=pk)
       serializer = SubtaskSerializer(subtask, context={'request': request})
       subtask.delete()
       return Response(serializer.data)

      
             
     
     