from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from .models import Users
from BEComputerVision.users.serializers import UsersSerializerCreate, UsersSerializerGetData
import uuid

class UsersViewSet(viewsets.ViewSet):
    """
    A simple Viewset for handling user actions.
    """

    queryset = Users.objects.all()
    serializer_class = UsersSerializerGetData

    @action(detail=False, methods=['get'], url_path="list-users")
    def list_users(self, request):
        users = self.queryset
        serializer = UsersSerializerGetData(users, many=True)
        
        return Response({
                         "status":200,
                         "message": "OK",
                         "data": serializer.data
                         })
    
    @action(detail=False, methods=['post'], url_path='create')
    def create_user(self, request):
        user_data = {
            'id': str(uuid.uuid4()),
            'is_verified': False,
        }

        allowed_fields = ['username', 'full_name', 'email', 'password']  # Các trường bạn muốn chấp nhận

        for field in allowed_fields:
            if field in request.data:
                user_data[field] = request.data[field]

        serializer = UsersSerializerCreate(data=user_data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "message": "Create new user successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': serializer.errors['email'][0]
            })