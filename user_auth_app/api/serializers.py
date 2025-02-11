from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    
    class Meta:
        model=User
        fields = ['username','first_name', 'last_name', 'email', 'password', 'repeated_password', 'is_staff']
        extra_kwargs = {
            'password':{
                'write_only': True
            }
        }
        
    def save(self):
        password = self.validated_data['password']
        repeated_password = self.validated_data['repeated_password']
        email= self.validated_data['email']
        username = self.validated_data['username']
        first_name=self.validated_data['first_name']
        last_name=self.validated_data['last_name']
        is_staff = self.validated_data.get('is_staff', 0)
        if password != repeated_password:
            raise serializers.ValidationError({'error':'password not correct'})
        if User.objects.filter(email = email).exists():
            return serializers.ValidationError({'error': 'email already exist'})
        account = User(email=email, username=username, first_name=first_name, last_name=last_name, is_staff=is_staff)
        account.set_password(password)
        account.save()
        return account
         