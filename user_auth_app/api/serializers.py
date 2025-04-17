from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles validation of unique username/email and password confirmation.
    """
    repeated_password = serializers.CharField(write_only=True)

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
            'password': {
                'write_only': True  # Do not include password in response data
            }
        }

    def validate(self, data):
        """
        Custom validation:
        - Checks if username and email are already taken
        - Ensures password and repeated password match
        """
        errors = {}
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        repeated_password = data.get('repeated_password')
        self.check_user_data(errors, username, email,password, repeated_password)
        return data
    
    def check_user_data(self, errors, username, email, password, repeated_password):
        if User.objects.filter(username=username).exists():
            errors['username'] = 'A user with this username already exists.'
        
        if User.objects.filter(email=email).exists():
            errors['email'] = 'A user with this email already exists.'
        
        if password != repeated_password:
            errors['password'] = "Passwords do not match."

        if errors:
            raise serializers.ValidationError(errors)
        
        

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


class LoginDataSerializer(serializers.Serializer):
    """
    Serializer for sending back login response data.
    """
    token = serializers.CharField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    user_id = serializers.IntegerField()
    email = serializers.EmailField()


class RegistrationDataSerializer(serializers.Serializer):
    """
    Serializer for sending back registration response data.
    """
    token = serializers.CharField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()