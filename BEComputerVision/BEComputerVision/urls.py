from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from BEComputerVision.product import views as views_product
from BEComputerVision.users import views as views_users

from rest_framework_simplejwt import views as jwt_views

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

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    
    path('api/login',  views_users.UserViewSetLogin.as_view({'post': 'login'}), name='user-login'),
    path('api/token/refresh', views_users.RefreshTokenView.as_view({'post': 'post'}), name='token_refresh'),
    
    path("api/users/list-users", views_users.UsersViewSetGetData.as_view({'get': 'list_users'}), name='user-list'),
    path("api/users/user-information/<uuid:id>", views_users.UsersViewSetGetData.as_view({'get': 'detail_user'}), name='user-information'),
    path("api/users/register", views_users.UsersViewSetCreate.as_view({'post': 'create'}), name='user-register'),
    path("api/users/change-information", views_users.UsersViewSetChangeInfor.as_view({'put': 'change_infor'}), name='change-information'),
    
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name = "schema"))
]
