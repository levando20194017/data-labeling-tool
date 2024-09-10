from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from BEComputerVision.product import views as views_product
from BEComputerVision.users import views as views_users

router = DefaultRouter()
# cấu hình router. list api
# product
router.register(r"category", views_product.CategoryViewSet)
router.register(r"brand", views_product.BrandViewSet)
router.register(r"product", views_product.ProductViewSet)

#user
router.register(r'users', views_users.UsersViewSetGetData, basename='users-list')
router.register(r'users', views_users.UsersViewSetCreate, basename='users-create')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    
    path("api/users/list-users/", views_users.UsersViewSetGetData.as_view({'get': 'list_users'}), name='user-list'),
    path("api/users/user-information/<str:id>/", views_users.UsersViewSetGetData.as_view({'get': 'detail_user'}), name='user-information'),
    path("api/users/create/", views_users.UsersViewSetCreate.as_view({'post': 'create'}), name='user-create'),
    
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name = "schema"))
]
