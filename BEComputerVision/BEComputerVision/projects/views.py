from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Projects
from BEComputerVision.users.models import Users
from BEComputerVision.roles.models import Roles
from BEComputerVision.projects.serializers import CreateProjectSerializer, ProjectSerializer, RenameProjectSerializer, RenameProjectSerializerShowListBodyData
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
from django.db import IntegrityError
# Load environment variables from .env file
load_dotenv()

        
class ProjectsViewSet(viewsets.ViewSet):
    """
    A simple Viewset for handling user actions.
    """
    authentication_classes = [SafeJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    #api get list projects
    serializer_class = ProjectSerializer
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
        
    #api detail project
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
    
    #api create new project
    serializer_class = CreateProjectSerializer
    @action(detail=False, methods=['post'], url_path="create-new-project")
    def create_project(self, request):
        """
        request body:
        - user_id: id of user
        - project_name: name of project (string and unique)
        - category: type of project. One of three options (Object Detection, Segmentation or Classification)
        """
        try:
            user_id = request.data.get('user_id')
            user = Users.objects.get(id=user_id)
            
            project_data = {}
            project_data['user'] = user_id #ở đây chỉ cần truyền lưu user_id vào trường user của bảng project
            allowed_fields = ['project_name', 'category']
            
            # Kiểm tra xem category có hợp lệ không
            if request.data['category'] not in ["Object Detection", "Segmentation", "Classification"]:
                return Response({
                    "status": 400,
                    "message": "Category field must be one of the following options: Object Detection, Segmentation, or Classification",
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Lấy dữ liệu từ request và bỏ vào project_data
            for field in allowed_fields:
                if field in request.data:
                    project_data[field] = request.data[field]
            
            # Khởi tạo serializer
            serializer = CreateProjectSerializer(data=project_data)
            
            if serializer.is_valid():
                try:
                    # Lưu dữ liệu vào database
                    serializer.save()
                    return Response({
                        "status": 200,
                        "message": "Create new project successfully!",
                    }, status=status.HTTP_201_CREATED)
                except IntegrityError:
                    # Bắt lỗi trùng tên dự án
                    return Response({
                        "status": 400,
                        "message": "A project with this name already exists. Please choose a different name.",
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Trả về lỗi nếu serializer không hợp lệ
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Create new project failed!',
                'errors': serializer.errors
            })
        
        except Users.DoesNotExist:
            # Bắt lỗi khi không tìm thấy user
            return Response({
                "status": 404,
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            # Bắt các lỗi ngoại lệ khác
            return Response({
                "status": 500,
                "message": "Internal server error: " + str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    
    #api rename project
    serializer_class = RenameProjectSerializerShowListBodyData
    @action(detail=False, methods=['put'], url_path="rename-project")
    def rename_project(self, request):
        try:
            user_id = request.data.get('user_id')
            new_project_name = request.data.get('project_name')
            project_id = request.data.get('project_id')
            
            user = Users.objects.get(id=user_id)
            project = Projects.objects.get(id = project_id, user = user) #trường user trong bảng project đang là 1 đối tượng
            project.project_name = new_project_name
            
            serializer = RenameProjectSerializer(instance=project, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": 200,
                    "message": "Change project_name successfully!",
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Users.DoesNotExist:
            # Bắt lỗi khi không tìm thấy user
            return Response({
                "status": 404,
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Projects.DoesNotExist:
            # Bắt lỗi khi không tìm thấy project
            return Response({
                "status": 404,
                "message": "Project not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            # Bắt các lỗi ngoại lệ khác
            return Response({
                "status": 500,
                "message": "Internal server error: " + str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
