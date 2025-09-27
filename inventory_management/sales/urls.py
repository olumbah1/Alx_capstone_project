from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('customers/', views.CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'),
    
    path('sales/', views.SaleListView.as_view(), name='sale-list'),
    path('sales/create/', views.SaleCreateView.as_view(), name='sale-create'),
    path('sales/<int:pk>/', views.SaleDetailView.as_view(), name='sale-detail'),
    
    path('dashboard/', views.sales_dashboard, name='sales-dashboard'),
    path('dashboard_analysis/', views.product_sales_analysis, name='sales-dashboard-analysis')
]