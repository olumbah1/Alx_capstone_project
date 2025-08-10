from .serialzer import StockMovementSerializer
from product.models import Product
from .models import StockMovement
from rest_framework import generics,filters
from rest_framework.permissions import IsAuthenticated
from django_filters import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import F, Sum

# Create your views here.

class StockMovementListCreateView(generics.ListCreateAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_class = [IsAuthenticated]
    filter_backends = [
           DjangoFilterBackend,
           filters.SearchFilter,    
    ]
    filter_fields = ['product', 'movement_type']
    search_fields = ['prdouct__name', 'reason']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
class StockMovementDetailView(generics.RetrieveUpdateDestroyAPIView):
        queryset = StockMovement.objects.all()
        serializer_class = StockMovementSerializer
        permission_classes = [IsAuthenticated]
            
class InventorySummaryView(generics.GenericsAPIView):
    def get(self, request):
        total_products = Product.object.count() # count Products
        
        total_stock = Product.objects.aggregate(Sum('current_stock')) ['current_stock_sum'] or 0
        
        # Count low stock products
        low_stock_count = Product.objects.filter(
            current_stock__lte=F('minimum_stock')
        ).count()
        
        # Count movements
        total_movements = StockMovement.objects.count()
        
        return Response({
            'total_products': total_products,
            'total_stock_items': total_stock,
            'low_stock_products': low_stock_count,
            'total_movements': total_movements
        })
    
class LowStockProductsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Product.objects.filter(current_stock__lte=F('minimum_stock'))
    
    def get_serializer_class(self):
        from products.serializers import ProductSerializer
        return ProductSerializer  
        
    