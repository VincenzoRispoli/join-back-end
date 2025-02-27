from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from user_auth_app.api.serializers import RegistrationSerializer, LoginDataSerializer, RegistrationDataSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from .factories import LoginData, RegistrationData

# Create your views here.

class RegistrationView(APIView):
    permission_classes = [AllowAny]
   
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data={}
        if serializer.is_valid():
          saved_account = serializer.save()
          token, created = Token.objects.get_or_create(user=saved_account)
          data = self.get_user_and_regist_data(saved_account, token)
        else:
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data)
    
    def get_user_and_regist_data(self, saved_account, token):
        user_data = RegistrationData(token.key, 
                                     saved_account.username,
                                     saved_account.first_name, 
                                     saved_account.last_name, 
                                     saved_account.is_staff, 
                                     saved_account.is_superuser,
                                     saved_account.email)
        user_data_serializer = RegistrationDataSerializer(user_data)
        return user_data_serializer.data
            
        
       
class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

   
    def post(self, request):
        username = request.data.get('username').strip()
        email = request.data.get('email').strip()
        password = request.data.get('password')
        user = self.custom_authentication(username, email, password)
        if not user:
            return Response({'ok': False, 'error': 'A User with given credentials, does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if serializer.is_valid():
               user = serializer.validated_data['user']
               return Response(self.success_response(user))
            else:
                return Response(self.validation_error_response(serializer)) 

    def success_response(self, user):
        login_data = self.get_user_and_login_data(user)
        return {
              'ok': True,
              'data': login_data,
              'status': status.HTTP_200_OK
          }
        
    def validation_error_response(self, serializer):
        return {
               'ok': False,
               'errors': serializer.errors,
               'status': status.HTTP_400_BAD_REQUEST
           }
       
    def get_user_and_login_data(self, user):
        token, created = Token.objects.get_or_create(user=user)
        login_data = LoginData(token.key, user.username, user.first_name, user.last_name, user.pk, user.email)
        login_data_serializer = LoginDataSerializer(login_data)
        return login_data_serializer.data
    
    
    def custom_authentication(self, username, email, password):
        try:
           user = User.objects.get(username = username, email = email)
           authenticated_user = authenticate(username=username, password=password)
           return authenticated_user
        except User.DoesNotExist:
               return None
     
           
    