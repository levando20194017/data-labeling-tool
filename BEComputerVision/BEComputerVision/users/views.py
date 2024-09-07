from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from .models import Users
from BEComputerVision.users.serializers import UsersSerializer

class UsersViewSet(viewsets.ViewSet):
    """
    A simple Viewset for handling user actions.
    """

    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    @action(detail=False, methods=['get'], url_path="list-users")
    def list_users(self, request):
        users = self.queryset
        serializer = UsersSerializer(users, many=True)
        
        return Response({
                         "status":200,
                         "message": "OK",
                         "data": serializer.data
                         })
    
    @action(detail=False, methods=['post'], url_path='create')  # Sử dụng url_path để tránh xung đột
    def create_user(self, request):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)