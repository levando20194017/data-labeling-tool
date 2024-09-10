from rest_framework import serializers

from .models import Users

class UsersSerializerGetData(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ['password']

class UsersSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'full_name', 'email', 'password']
        
class UsersSerializerLogin(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'password']
