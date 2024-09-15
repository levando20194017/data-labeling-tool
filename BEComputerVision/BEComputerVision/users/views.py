import jwt
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Users
from BEComputerVision.users.serializers import UsersSerializerCreate, UsersSerializerGetData, UsersSerializerLogin, RefreshTokenSerializer
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
import random
import smtplib
from rest_framework.permissions import IsAuthenticated
from BEComputerVision.users.authentication import SafeJWTAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action, permission_classes
from BEComputerVision.users.utils import generate_access_token, generate_refresh_token
from rest_framework import exceptions
import os
from dotenv import load_dotenv
# from django.views.decorators.csrf import ensure_csrf_cookie

# Load environment variables from .env file
load_dotenv()

class UsersViewSetGetData(viewsets.ViewSet):
    """
    A simple Viewset for handling user actions.
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializerGetData
    
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [IsAuthenticated] #cái này là áp dụng cho toàn bộ view
    # @permission_classes([IsAuthenticated]) #cái này là áp dụng quyền cho từng view khác nhau
    
    #api get all users
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('page_index', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Index of the page'),
        openapi.Parameter('page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Number of items per page'),
    ])
    @action(detail=False, methods=['get'], url_path="list-users")
    # @ensure_csrf_cookie
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

@permission_classes([AllowAny])       
class UsersViewSetCreate(viewsets.ViewSet):
    """
    A simple Viewset for handling user actions.
    """

    queryset = Users.objects.all()
    serializer_class = UsersSerializerCreate
    
    #api create new user
    @action(detail=False, methods=['post'], url_path='register')
    def create_user(self, request):
        user_data = {}

        allowed_fields = ['username', 'full_name', 'email', 'password']  # Các trường bạn muốn chấp nhận

        for field in allowed_fields:
            if field in request.data:
                user_data[field] = request.data[field]

        # # Tạo mã xác nhận 6 chữ số
        # confirmation_code = ''.join(random.choices('0123456789', k=6))

        # # Địa chỉ email người gửi
        # sender_email = 'levando0708@gmail.com'

        # # Gửi email chứa mã xác nhận
        # send_mail(
        #     'Xác nhận đăng ký',
        #     f'Mã xác nhận của bạn là: {confirmation_code}',
        #     sender_email,
        #     [user_data['email']],
        #     fail_silently=False,
        # )

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

@permission_classes([AllowAny])
class UserViewSetLogin(viewsets.ViewSet):
    """
    A simple Viewset for handling user actions.
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializerLogin
    @action(detail=False, methods=['post'], url_path='login')
    # @ensure_csrf_cookie
    def login(self, request):
        try:
            user = Users.objects.get(email=request.data['email'], password=request.data['password'])
            serializer_user = UsersSerializerGetData(user)
            # refresh = RefreshToken.for_user(user)
            
            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)
            
            # response = Response()
            # response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
            if not user.is_verified:
                return Response({
                    "status": 201,
                    "message": "This account is not verified.", 
                })
            else:       
                return Response({
                    "status": 200,
                    "message": "OK",
                    "data": {
                            'access_token': access_token,
                            'refresh_token': refresh_token,
                            'user_infor': serializer_user.data
                        }
                    })
        except Users.DoesNotExist:
            return Response({
                "status": 404,
                "message": "Invalid email or password"
            }, status=404)
            
@permission_classes([AllowAny])
class RefreshTokenView(viewsets.ViewSet):
    serializer_class = RefreshTokenSerializer
    
    @action(detail=False, methods=['post'], url_path='token/refresh/')
    def post(self, request):
        refresh_token = request.data['refresh_token']
        
        if refresh_token is None:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.')
        try:
            payload = jwt.decode(
                refresh_token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'expired refresh token, please login again.')

        user = Users.objects.filter(id=payload.get('user_id')).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_verified:
            raise exceptions.AuthenticationFailed('user is inactive')

        access_token = generate_access_token(user)
        return Response({
            'status': 200,
            'message': "OK",
            'data': {
                'access_token': access_token
            }
            })
    
    
            