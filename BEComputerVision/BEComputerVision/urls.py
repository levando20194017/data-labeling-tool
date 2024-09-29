from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view

from BEComputerVision.product import views as views_product
from BEComputerVision.users import views as views_users
from BEComputerVision.projects import views as views_projects

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Your API Title",
#         default_version='v1',
#         description="API documentation",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="contact@yourapi.local"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
# )

router = DefaultRouter()
# cấu hình router. list api
# product
router.register(r"category", views_product.CategoryViewSet)
router.register(r"brand", views_product.BrandViewSet)
router.register(r"product", views_product.ProductViewSet)

#user
router.register(r'users', views_users.UsersViewSetGetData, basename='users-list')
router.register(r'users', views_users.UsersViewSetCreate, basename='users-register')
# router.register(r'users', views_users.UserViewSetLogin, basename='users-login')

#projects
router.register(r'projects', views_projects.ProjectsViewSet, basename='list-projects')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    
    path('api/login/',  views_users.UserViewSetLogin.as_view({'post': 'login'}), name='user-login'),
    path('api/token/refresh/', views_users.RefreshTokenView.as_view({'post': 'post'}), name='token_refresh'),
    
    #users
    path("api/users/list-users/", views_users.UsersViewSetGetData.as_view({'get': 'list_users'}), name='user-list'),
    path("api/users/user-information/<uuid:id>/", views_users.UsersViewSetGetData.as_view({'get': 'detail_user'}), name='user-information'),
    path("api/users/register/", views_users.UsersViewSetCreate.as_view({'post': 'create_user'}), name='user-register'),
    path("api/users/change-information/", views_users.UsersViewSetChangeInfor.as_view({'put': 'change_infor'}), name='change-information'),
    path("api/users/change-avatar/", views_users.ChangeAvatarAPI.as_view({'put': 'change_avatar'}), name='change-avatar'),
    #projects
    path("api/projects/list-projects/", views_projects.ProjectsViewSet.as_view({'get': 'list_projects'}), name='list-projects'),
    path("api/projects/project-information/<uuid:id>/", views_projects.ProjectsViewSet.as_view({'get': 'detail_project'}), name='project-information'),
    path("api/projects/create-new-project/", views_projects.ProjectsViewSet.as_view({'post': 'create_project'}), name='create-new-project'),
   
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), 
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name = "schema"))
]
