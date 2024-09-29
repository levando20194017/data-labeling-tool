from rest_framework import serializers
from .models import Projects

class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['project_name', 'category', 'user']
        
class RenameProjectSerializerShowListBodyData(serializers.ModelSerializer):
    #Cái này chỉ để show các trường lên swagger thôi nha
    user_id = serializers.UUIDField(required=True)
    project_id = serializers.UUIDField(required=True) 
    class Meta:
        model = Projects
        fields = ['user_id', 'project_id', 'project_name']
        
class RenameProjectSerializer(serializers.ModelSerializer):
    #xét chỉ thay đổi mỗi trường project_name
    #nếu sửa đổi trường để lưu vào thì mình có thể thay đổi nhưng mà mình phải map cái trường đó gắn với cái trường trong bảng DB
    class Meta:
        model = Projects
        fields = ['project_name']
        
class ProjectSerializer(serializers.ModelSerializer):
    #ví dụ lấy thông tin ra mà muốn trả về thêm trường thì mình tạo nó. Ở đây t muốn trả thêm trường creator
    #chú ý là cái này để để lấy thông tin ra thôi nha, còn nếu mà thực hiện save vào DB thì phải tạo cái serializer mới với fields là các trường mình muốn thay đổi và nó map với trường trong bảng DB
    creator = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Projects
        fields = ['id','project_name', 'category', 'creator', 'created_at', 'updated_at']
    
