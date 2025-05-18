from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles validation of unique username/email and password confirmation.
    """
    repeated_password = serializers.CharField(
        write_only=True, allow_blank=True, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'repeated_password',
            'is_staff'
        ]
        extra_kwargs = {
            'username': {'required': False, 'allow_blank': True},
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
            'email': {'required': False, 'allow_blank': True},
            'password': {'write_only': True, 'required': False, 'allow_blank': True},
        }
    
    def validate_username(self, value):
        """
        Validates the 'username' field.

        Ensures that the username is at least 3 characters long and 
        does not already exist in the database.

        Args:
            value (str): The input username to validate.

        Raises:
            serializers.ValidationError: If the username is too short or already taken.

        Returns:
            str: The validated username.
        """
        if not value or len(value) < 3:
            raise serializers.ValidationError('Please insert a username with at least 3 characters')
        elif User.objects.filter(username=value).exists():
            raise serializers.ValidationError('A user with this username already exists.')
        return value

    def validate_first_name(self, value):
        """
        Validates the 'first_name' field.

        Ensures that the first name is at least 3 characters long.

        Args:
            value (str): The input first name to validate.

        Raises:
            serializers.ValidationError: If the first name is too short.

        Returns:
            str: The validated first name.
        """
        if not value or len(value) < 3:
            raise serializers.ValidationError('Please insert a first name with at least 3 characters')
        return value

    def validate_last_name(self, value):
        """
        Validates the 'last_name' field.

        Ensures that the last name is at least 3 characters long.

        Args:
            value (str): The input last name to validate.

        Raises:
            serializers.ValidationError: If the last name is too short.

        Returns:
            str: The validated last name.
        """
        if not value or len(value) < 3:
            raise serializers.ValidationError('Please insert a last name with at least 3 characters')
        return value

    def validate_email(self, value):
        """
        Validates the 'email' field.

        Ensures that the email is provided and is not already registered in the system.

        Args:
            value (str): The input email to validate.

        Raises:
            serializers.ValidationError: If the email is empty or already used.

        Returns:
            str: The validated email.
        """
        if not value:
            raise serializers.ValidationError('Please insert an user email')
        elif User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def validate_password(self, value):
        """
        Validates the 'password' field.

        Ensures that the password is at least 8 characters long.

        Args:
            value (str): The input password to validate.

        Raises:
            serializers.ValidationError: If the password is too short.

        Returns:
            str: The validated password.
        """
        if not value or len(value) < 8:
            raise serializers.ValidationError('Please insert a password with at least 8 characters')
        return value

    def validate(self, data):
        """
        Performs object-level validation.

        Ensures that the 'password' and 'repeated_password' fields match.

        Args:
            data (dict): The input data to validate.

        Raises:
            serializers.ValidationError: If the passwords do not match.

        Returns:
            dict: The validated data.
        """
        password = data.get('password')
        repeated_password = data.get('repeated_password')
        
        if password != repeated_password:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data


    def create(self, validated_data):
        """
        Creates a new user instance after successful validation.
        Automatically sets is_staff and is_superuser to True.
        """
        # Extract validated fields
        username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        password = validated_data['password']

        # Create the user instance
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=True,         # Mark user as staff (custom choice)
            is_superuser=True      # Also make user a superuser
        )
        user.set_password(password)
        user.save()
        return user


class CustomLoginSerializer(serializers.ModelSerializer):
    """
    Serializer used for handling user login with either email and password.

    Fields:
        - username: Optional field, not used for authentication directly.
        - email: Optional field used for identifying the user.
        - password: Required for authentication. Write-only for security.
    """
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, allow_blank=True)

    class Meta:
        """
        Meta configuration for the serializer.

        Uses the built-in Django User model and includes all fields.
        """
        model = User
        fields = '__all__'

    def validate(self, data):
        """
        Object-level validation for login.

        Validates the presence of a password, checks if an email is provided,
        ensures the user exists, and authenticates them using the email and password.

        Args:
            data (dict): Dictionary containing 'email' and 'password' keys.

        Raises:
            serializers.ValidationError: If any validation fails:
                - Password is missing
                - Email is not provided or invalid
                - User does not exist
                - Authentication fails

        Returns:
            dict: The validated data, including the authenticated user instance under 'user'.
        """
        email = data.get('email')
        password = data.get('password')
        errors = {}

        # Check if password is provided
        if not password:
            errors['password'] = 'Please insert a user password'
        user = None

        # If email is provided, try to fetch user and authenticate
        if email:
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(
                    username=user_obj.username, password=password)
            except User.DoesNotExist:
                errors['email'] = 'A user with this email does not exist'
        # If email is not provided or blank, add error
        elif not email or len(email) == 0:
            errors['email'] = 'Please insert a user email in the right format [@...de/com/it/]'

        # If authentication fails, raise an error
        if not user:
            errors['user'] = 'User does not exist'
        
        # If any errors were collected, raise a ValidationError
        if errors:
            raise serializers.ValidationError(errors)

        # Add authenticated user to the validated data
        data['user'] = user
        return data