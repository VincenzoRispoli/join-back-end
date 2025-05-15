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
        if not value or len(value) < 3:
            raise serializers.ValidationError('Please insert a username with at least 3 characters')
        elif User.objects.filter(username=value).exists():
            raise serializers.ValidationError('A user with this username already exists.')
        return value
    
    def validate_first_name(self, value):
        if not value or len(value) < 3:
            raise serializers.ValidationError('Please insert a first name with at least 3 characters')
        return value
    
    def validate_last_name(self, value):
        if not value or len(value) < 3:
            raise serializers.ValidationError('Please insert a last name with at least 3 characters')
        return value
    
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError('Please insert an user email')
        elif User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value
    
    def validate_password(self, value):
        if not value or len(value) < 8:
            raise serializers.ValidationError('Please insert a password with at least 8 characters')
        return value
    
    def validate(self, data):
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
