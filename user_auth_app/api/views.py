
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
    """
    API view that handles user registration.
    Allows registration of standard users and handles guest user logic.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles POST requests for user registration.

        If the username is 'Guest', attempts to retrieve or register the guest user.
        Otherwise, proceeds with standard user registration.

        Args:
            request (Request): The incoming HTTP request containing user data.

        Returns:
            Response: A DRF Response object containing either user data or error messages.
        """
        username = request.data.get('username')
        if username == 'Guest':
            return self.get_or_regist_guest_user(request)
        else:
            return self.regist_user(request)

    def get_or_regist_guest_user(self, request):
        """
        Attempts to retrieve the guest user and return their data.
        If the guest user does not exist, proceeds with registration.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            Response: A DRF Response object containing guest user data or result of registration.
        """
        data = {}
        try:
            data = self.get_data_of_guest_user()
            return Response({'data': data, 'ok': True})
        except User.DoesNotExist:
            return self.regist_user(request)

    def regist_user(self, request):
        """
        Registers a new user with the provided request data.

        Validates the data using RegistrationSerializer.
        Returns a success response if valid, or an error response if invalid.

        Args:
            request (Request): The incoming HTTP request with registration data.

        Returns:
            Response: A DRF Response object containing user data or validation errors.
        """
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            data = self.get_data_of_registered_user(serializer)
            return Response({'data': data, 'ok': True, 'message': 'Account succesfully created'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'data': serializer.errors, 'ok': False, 'message': 'Something went wrong while creating your account. Please try again'}, status=status.HTTP_400_BAD_REQUEST)

    def get_data_of_guest_user(self):
        """
        Retrieves guest user data and authentication token.

        Returns:
            dict: A dictionary containing the guest user's data and token.

        Raises:
            User.DoesNotExist: If the guest user does not exist in the database.
        """
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
        return data

    def get_data_of_registered_user(self, serializer):
        """
        Saves the user instance from the validated serializer and generates a token.

        Args:
            serializer (RegistrationSerializer): A validated serializer instance.

        Returns:
            dict: A dictionary containing the registered user's data and token.
        """
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
        return data


class CustomLoginView(APIView):
    """
    API view that handles user login.
    Accepts login credentials, validates them, and returns a token and user data if successful.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles POST requests for user login.

        Validates the request data using CustomLoginSerializer.
        Returns user data and token if login is successful, or error messages if not.

        Args:
            request (Request): The incoming HTTP request containing login data.

        Returns:
            Response: A DRF Response object with either login success data or error messages.
        """
        serializer = CustomLoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            data = self.get_logged_user_data(serializer)
            return Response({'data': data, 'ok': True, 'message': 'User successfuly logged'}, status=status.HTTP_200_OK)
        else:
            return Response({'data': serializer.errors, 'ok': False, 'message': 'Login failed'}, status=status.HTTP_400_BAD_REQUEST)

    def get_logged_user_data(self, serializer):
        """
        Retrieves authenticated user from validated serializer data and generates a token.

        Args:
            serializer (CustomLoginSerializer): A validated serializer instance containing the user.

        Returns:
            dict: A dictionary containing the user's token and public data.
        """
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
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
        return data
