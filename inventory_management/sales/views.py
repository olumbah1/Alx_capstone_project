from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import CustomerSerializer, SaleSerializer, SaleCreateSerializer
from django.db.models import Sum, Count, F, Avg
from django.db import transaction
from .models import Customer, Sale, SaleItem
from products.models import Product

# Create your views here.

# CUSTOMER VIEWS
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'email', 'phone']
    ordering = ['name']

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# SALE VIEWS
class SaleListView(generics.ListAPIView):
    queryset = Sale.objects.select_related('customer', 'created_by').prefetch_related('items')
    serializer_class = SaleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['payment_status', 'customer']
    search_fields = ['sale_number', 'customer__name']
    ordering = ['-created_at']

class SaleCreateView(generics.CreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleCreateSerializer
    
    def perform_create(self, serializer):
        #  Use transaction to ensure data consistency
        with transaction.atomic():
            serializer.save(created_by=self.request.user)

class SaleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.select_related('customer').prefetch_related('items')
    serializer_class = SaleSerializer
    
    

# ENHANCED DASHBOARD WITH YOUR PRODUCT DATA
@api_view(['GET'])
def sales_dashboard(request):
    """Enhanced dashboard using your Product model features"""
    
    # Basic sales stats
    total_sales = Sale.objects.count()
    total_revenue = Sale.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    pending_sales = Sale.objects.filter(payment_status='pending').count()
    
    # STOCK ALERTS - Using your is_low_stock property
    low_stock_products = []
    for product in Product.objects.all():
        if product.is_low_stock:
            low_stock_products.append({
                'id': product.id,
                'name': product.name,
                'current_stock': product.quantity,
                'threshold': product.low_stock_threshold,
                'category': product.category.name,
                'total_value': float(product.total_value)
            })
    
    # TOP SELLING PRODUCTS
    top_selling = SaleItem.objects.values(
        'product__name',
        'product__category__name'
    ).annotate(
        total_sold=Sum('quantity'),
        total_revenue=Sum('total_price')
    ).order_by('-total_sold')[:5]
    
    # TOP CUSTOMERS
    top_customers = Customer.objects.annotate(
        total_spent=Sum('sale__total_amount'),
        sales_count=Count('sale')
    ).order_by('-total_spent')[:5]
    
    # RECENT SALES
    recent_sales = Sale.objects.select_related('customer').order_by('-created_at')[:5]
    recent_sales_data = []
    for sale in recent_sales:
        recent_sales_data.append({
            'id': sale.id,
            'sale_number': sale.sale_number,
            'customer_name': sale.customer.name,
            'total_amount': float(sale.total_amount),
            'payment_status': sale.payment_status,
            'items_count': sale.items.count()
        })
    
    return Response({
        'summary': {
            'total_sales': total_sales,
            'total_revenue': float(total_revenue),
            'pending_sales': pending_sales,
            'low_stock_alerts': len(low_stock_products),
        },
        'low_stock_products': low_stock_products,
        'top_selling_products': list(top_selling),
        'top_customers': [
            {
                'name': customer.name,
                'total_spent': float(customer.total_spent or 0),
                'sales_count': customer.sales_count
            } for customer in top_customers
        ],
        'recent_sales': recent_sales_data,
    })

# 🔍 PRODUCT SALES ANALYSIS
@api_view(['GET'])
def product_sales_analysis(request, product_id):
    """Analyze sales for a specific product"""
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    
    # Sales data for this product
    sale_items = SaleItem.objects.filter(product=product)
    
    total_sold = sale_items.aggregate(total=Sum('quantity'))['total'] or 0
    total_revenue = sale_items.aggregate(total=Sum('total_price'))['total'] or 0
    average_price = sale_items.aggregate(avg=Avg('unit_price'))['avg'] or 0
    
    return Response({
        'product': {
            'id': product.id,
            'name': product.name,
            'catalog_price': float(product.price),
            'current_stock': product.quantity,
            'is_low_stock': product.is_low_stock,
            'category': product.category.name,
        },
        'sales_stats': {
            'total_sold': total_sold,
            'total_revenue': float(total_revenue),
            'average_selling_price': float(average_price),
            'times_sold': sale_items.values('sale').distinct().count(),
        }
    })
