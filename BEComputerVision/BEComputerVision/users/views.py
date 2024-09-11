from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from .models import Users
from BEComputerVision.users.serializers import UsersSerializerCreate, UsersSerializerGetData, UsersSerializerLogin
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.core.mail import send_mail
import random
import smtplib

class UsersViewSetGetData(viewsets.ViewSet):
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
        
    #api detail user
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('id', in_=openapi.IN_PATH, type=openapi.TYPE_STRING, description='ID of the user'),
    ])
    @action(detail=False, methods=['get'], url_path="user-information/(?P<id>[^/]+)")
    def detail_user(self, request, id=None):
        """
        Get details of a specific user based on ID.

        Parameters:
        - id: The ID of the user to retrieve.
        """
        if id is None:
            return Response({
                "status": 400,
                "message": "ID parameter is required."
            }, status=400)

        try:
            user = Users.objects.get(id=id)
            serializer = UsersSerializerGetData(user)
            return Response({
                "status": 200,
                "message": "OK",
                "data": serializer.data
            })
        except Users.DoesNotExist:
            return Response({
                "status": 404,
                "message": "User not found."
            }, status=404)
        except ValidationError:
            return Response({
                "status": 400,
                "message": "Invalid ID format."
            }, status=400)
        
class UsersViewSetCreate(viewsets.ViewSet):
    """
    A simple Viewset for handling user actions.
    """

    queryset = Users.objects.all()
    serializer_class = UsersSerializerCreate
    
    #api create new user
    @action(detail=False, methods=['post'], url_path='create')
    def create_user(self, request):
        user_data = {}

        allowed_fields = ['username', 'full_name', 'email', 'password']  # Các trường bạn muốn chấp nhận

        for field in allowed_fields:
            if field in request.data:
                user_data[field] = request.data[field]

        # Tạo mã xác nhận 6 chữ số
        confirmation_code = ''.join(random.choices('0123456789', k=6))

        # Địa chỉ email người gửi
        sender_email = 'levando0708@gmail.com'

        # Gửi email chứa mã xác nhận
        send_mail(
            'Xác nhận đăng ký',
            f'Mã xác nhận của bạn là: {confirmation_code}',
            sender_email,
            [user_data['email']],
            fail_silently=False,
        )

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
        
class UserViewSetLogin(viewsets.ViewSet):
    """
    A simple Viewset for handling user actions.
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializerLogin
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        try:
            user = Users.objects.get(email=request.data['email'], password=request.data['password'])
            serializer = UsersSerializerGetData(user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "status": 200,
                "message": "OK",
                "data": {
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh),
                        'user_infor': serializer.data
                    }
                })
        except Users.DoesNotExist:
            return Response({
                "status": 404,
                "message": "Invalid email or password"
            }, status=404)