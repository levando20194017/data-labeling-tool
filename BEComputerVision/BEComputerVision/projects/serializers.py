from rest_framework import serializers
from .models import Projects

class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['project_name', 'category', 'user']
        
class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.UUIDField(source='user.username', read_only=True)
    class Meta:
        model = Projects
        fields = ['id','project_name', 'category', 'creator', 'created_at', 'updated_at']
    
