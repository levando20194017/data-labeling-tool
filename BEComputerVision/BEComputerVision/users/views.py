from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from .models import Users
from BEComputerVision.users.serializers import UsersSerializerCreate, UsersSerializerGetData
import uuid
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UsersViewSet(viewsets.ViewSet):
    """
    A simple Viewset for handling user actions.
    """

    queryset = Users.objects.all()
    serializer_class = UsersSerializerGetData

    #api get all users
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('page_index', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Index of the page'),
        openapi.Parameter('page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Number of items per page'),
    ])
    @action(detail=False, methods=['get'], url_path="list-users")
    def list_users(self, request):
        """
        List users with pagination.

        Parameters:
        - page_index: The index of the page (default is 1).
        - page_size: The number of items per page (default is 10).
        """
        page_index = int(request.GET.get('page_index', 1))
        page_size = int(request.GET.get('page_size', 10))

        paginator = Paginator(self.queryset, page_size)
        try:
            users = paginator.page(page_index)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        serializer = UsersSerializerGetData(users, many=True)

        return Response({
            "status": 200,
            "message": "OK",
            "data": {
                "total_pages": paginator.num_pages,
                "data": serializer.data
                }
        })
    
    #api create new user
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