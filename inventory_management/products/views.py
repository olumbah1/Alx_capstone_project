from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, F

# Create your views here.
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]  
    
    filterset_fields = ['category']
    search_fields = ['name','description']
    
    def get_queryset(self):
        queryset = Product.objects.all()
        low_stock = self.request.query_params.get('low_stock', None)
        
        if low_stock == 'true':
            queryset = queryset.filter(current_stock__lte=F('minimum_stock'))
        return queryset
    
    def perform_create(self, serializers):
        serializers.save(user=self.request.user)
        
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    
class CategoryListCreateView(generics.ListCreateView):
    queryset = Category.object.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
