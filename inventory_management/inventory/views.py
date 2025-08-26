from .serializers import StockMovementSerializer
from products.models import Product
from .models import StockMovement
from rest_framework import generics,filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import F, Sum

# Create your views here.

class StockMovementListCreateView(generics.ListCreateAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
           DjangoFilterBackend,
           filters.SearchFilter,    
    ]
    filterset_fields = ['product', 'movement_type']
    search_fields = ['product__name', 'reason']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
class StockMovementDetailView(generics.RetrieveUpdateDestroyAPIView):
        queryset = StockMovement.objects.all()
        serializer_class = StockMovementSerializer
        permission_classes = [IsAuthenticated]
            

class InventorySummaryView(generics.GenericAPIView):
    def get(self, request):
        total_products = Product.objects.count()

        total_stock = Product.objects.aggregate(
            total=Sum('quantity')
        )['total'] or 0

        low_stock_count = Product.objects.filter(
            quantity__lte=F('low_stock_threshold')
        ).count()

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
        
    