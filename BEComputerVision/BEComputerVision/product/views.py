from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Category, Brand, Product
from BEComputerVision.product.serializers import CategorySerializer, BrandSerializer, ProductSerializer

class CategoryViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all Categories
    """
    
    queryset = Category.objects.all()
    
    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        
        return Response({
                         "status":200,
                         "message": "OK",
                         "data": serializer.data
                         })
        
class BrandViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all brands
    """
    queryset = Brand.objects.all()
    
    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        
        return Response({
                         "status":200,
                         "message": "OK",
                         "data": serializer.data
                         })
        
class ProductViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all brands
    """
    queryset = Product.objects.all()
    
    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        
        return Response({
                         "status":200,
                         "message": "OK",
                         "data": serializer.data
                         })        