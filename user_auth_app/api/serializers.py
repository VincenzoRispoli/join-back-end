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

    def validate(self, data):
        """
        Custom validation:
        - Checks if username and email are already taken
        - Ensures password and repeated password match
        """
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        repeated_password = data.get('repeated_password')
        self.check_user_data(username, first_name, last_name, email,
                             password, repeated_password)
        return data

    def check_user_data(self, username, first_name, last_name, email, password, repeated_password):
        errors = {}
        if not username or len(username) < 3:
            errors['username'] = 'Please insert a username with at least 3 characters'
        elif User.objects.filter(username=username).exists():
            errors['username'] = 'A user with this username already exists.'
        if not first_name or len(first_name) < 3:
            errors['first_name'] = 'Please insert a first name with at least 3 characters'
        if not last_name or len(last_name) < 3:
            errors['last_name'] = 'Please insert a last name with at least 3 characters'
        if not email:
            errors['email'] = 'Please insert an user email'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'A user with this email already exists.'
        if not password or len(password) < 8:
            errors['password'] = 'Please insert a password with at least 8 characters'
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


class CustomLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, allow_blank=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        errors = {}

        if not password:
            errors['password'] = 'Please insert a user password'
        user = None

        if email:
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(
                    username=user_obj.username, password=password)
            except User.DoesNotExist:
                errors['email'] = 'A user with this email does not exist'
        elif not email or len(email) == 0:
            errors['email'] = 'Please insert a user email in the right format [@...de/com/it/]'

        if not user:
            errors['user'] = 'User does not exist'
        
        if errors:
            raise serializers.ValidationError(errors)
        data['user'] = user
        return data
