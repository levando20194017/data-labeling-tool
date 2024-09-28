from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Projects
from BEComputerVision.users.models import Users
from BEComputerVision.roles.models import Roles
from BEComputerVision.projects.serializers import ProjectListSerializer, ProjectSerializer
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from BEComputerVision.users.authentication import SafeJWTAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from dotenv import load_dotenv
from django.db.models import Q
# Load environment variables from .env file
load_dotenv()

        
class ProjectsViewSetGetData(viewsets.ViewSet):
    """
    A simple Viewset for handling user actions.
    """
    serializer_class = ProjectSerializer
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=['get'], url_path="list-projects")
    def list_projects(self, request,):
        """
        List projects with pagination.

        Parameters:
        - page_index: The index of the page (default is 1).
        - page_size: The number of items per page (default is 10).
        - user_id:  id of user
        - type: choose 1 of 2 options "My Projects" or "Collaboration" (string)
        """
        page_index = int(request.query_params.get('page_index', 1))  # Use query_params for GET requests
        page_size = int(request.query_params.get('page_size', 10))
        user_id = request.query_params.get('user_id')
        project_type = request.query_params.get('type')

        if not user_id:
            return Response({"status": 400, "message": "User ID is required"}, status=400)

        if project_type == "My Projects":
            # Get projects created by the user or where the user has a role
            projects = Projects.objects.filter(user_id=user_id)
        else:
            # Get projects where the user has a role
            user_role_projects = Roles.objects.filter(user_id=user_id).values_list('project_id', flat=True)

            # Lấy danh sách các dự án mà người dùng đã tạo
            user_created_projects = Projects.objects.filter(user_id=user_id).values_list('id', flat=True)

            # Lọc ra các dự án mà người dùng có vai trò nhưng không phải là dự án họ đã tạo
            projects = Projects.objects.filter(id__in=user_role_projects).exclude(id__in=user_created_projects)

        paginator = Paginator(projects, page_size)

        try:
            paginated_projects = paginator.page(page_index)
        except PageNotAnInteger:
            paginated_projects = paginator.page(1)
        except EmptyPage:
            paginated_projects = paginator.page(paginator.num_pages)

        serializer = ProjectSerializer(paginated_projects, many=True)

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
    @action(detail=False, methods=['get'], url_path="project-information/(?P<id>[^/]+)")
    def detail_project(self, request, id=None):
        """
        Get details of a specific user based on ID.

        Parameters:
        - id: The ID of the project to retrieve.
        """
        if id is None:
            return Response({
                "status": 400,
                "message": "ID parameter is required."
            }, status=400)

        try:
            project = Projects.objects.get(id=id)
            serializer = ProjectSerializer(project)
            return Response({
                "status": 200,
                "message": "OK",
                "data": serializer.data
            })
        except Projects.DoesNotExist:
            return Response({
                "status": 404,
                "message": "Project not found."
            }, status=404)
        except ValidationError:
            return Response({
                "status": 400,
                "message": "Invalid ID format."
            }, status=400)