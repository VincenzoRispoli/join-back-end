
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from user_auth_app.api.serializers import RegistrationSerializer, CustomLoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from django.contrib.auth.models import User

# Create your views here.


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        if username == 'Guest':
            try:
                guest_user = User.objects.get(username='Guest')
                token, _ = Token.objects.get_or_create(user=guest_user)
                data = {
                    'token': token.key,
                    'username': guest_user.username,
                    'first_name': guest_user.first_name,
                    'last_name': guest_user.last_name,
                    'email': guest_user.email,
                    'is_staff': guest_user.is_staff,
                    'is_superuser': guest_user.is_superuser
                }
                return Response({'data': data, 'ok':True})
            except User.DoesNotExist:
                pass
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'first_name': saved_account.first_name,
                'last_name': saved_account.last_name,
                'email': saved_account.email,
                'is_staff': saved_account.is_staff,
                'is_superuser': saved_account.is_superuser,
            }
            return Response({'data': data, 'ok': True, 'message': 'Account succesfully created'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'data': serializer.errors, 'ok': False, 'message': 'Something went wrong while creating your account. Please try again'}, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomLoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            print(user)
            print(user.id)
            data = {
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser
            }
            return Response({'data': data, 'ok': True, 'message': 'User successfuly logged'}, status=status.HTTP_200_OK)
        else:
            return Response({'data': serializer.errors, 'ok': False, 'message': 'Login failed'}, status=status.HTTP_400_BAD_REQUEST)
