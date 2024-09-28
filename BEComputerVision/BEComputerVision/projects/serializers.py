from rest_framework import serializers
from .models import Projects

class ProjectListSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField()
    page_index = serializers.IntegerField(required=True)
    page_size = serializers.IntegerField(required=True)
    type = serializers.CharField(required=True)
    class Meta:
        model = Projects
        fields = '__all__'
        
class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.UUIDField(source='user.username', read_only=True)
    class Meta:
        model = Projects
        fields = ['id','project_name', 'category', 'creator', 'created_at', 'updated_at']
    
