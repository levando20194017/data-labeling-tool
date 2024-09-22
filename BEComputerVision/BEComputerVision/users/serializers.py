from rest_framework import serializers
from .models import Users

class UsersSerializerGetData(serializers.ModelSerializer):
    id = serializers.UUIDField()  # Thêm trường id kiểu UUID vào Serializer
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
        
class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True, help_text="The refresh token")

class UsersSerializerChangeInfor(serializers.ModelSerializer):
    user_id = serializers.CharField(required=True, help_text="The refresh token")
    class Meta:
        model = Users
        exclude = ['id', 'email', 'password', 'img_url', 'role', 'is_verified']
        
class UsersSerializerChangePassword(serializers.ModelSerializer):
    user_id = serializers.CharField(required=True, help_text="The refresh token")
    password = serializers.CharField(required=True, help_text="The refresh token")
    
class UsersSerializerChangeAvatar(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['img_url']