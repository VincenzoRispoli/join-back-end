from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from user_auth_app.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

# Create your views here.

@api_view(['GET', 'POST'])
def user_test_view(request):
    return Response({'message': 'ciao bello'})

class RegistrationView(APIView):
    permission_classes = [AllowAny]
   
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data={}
        if serializer.is_valid():
          saved_account = serializer.save()
          token, created = Token.objects.get_or_create(user=saved_account)
          data = {
              'token': token.key,
              'username': saved_account.username,
              'first_name': saved_account.first_name,
              'last_name': saved_account.last_name,
              'is_staff':saved_account.is_staff,
              'email': saved_account.email
          }
        else:
           return Response(serializer.errors)
        return Response(data)
    
class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
   
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data={}
        if serializer.is_valid():
          user = serializer.validated_data['user']
          token, created = Token.objects.get_or_create(user=user)
          print("The token are:", Token.objects.all())
          data = {
              'token': token.key,
              'username': user.username,
              'first_name': user.first_name,
              'last_name': user.last_name,
              'user_id': user.pk,
              'email': user.email
          }
          return Response({
              'ok': True,
              'data': data,
              'status': status.HTTP_200_OK
          })
        else:
           return Response({
               'ok': False,
               'errors': serializer.errors,
               'status': status.HTTP_400_BAD_REQUEST
           })   
    