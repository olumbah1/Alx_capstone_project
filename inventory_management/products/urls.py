from django.urls import path
from .views import ProductListCreateView, ProductDetailView, CategoryListCreateView, CategoryDetailView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name = 'product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name = 'product-detail'),
    path('category/', CategoryListCreateView.as_view(), name = 'category-list'),
    path('category/<int:pk/', CategoryDetailView.as_view(), name = 'category-detail')
]

urlpatterns = [
    path('movements/', StockMovementListCreateView.as_view()),
    path('movements/<int:pk>/', StockMovementDetailView.as_view()),
    path('summary/', InventorySummaryView.as_view()),
    path('low-stock/', LowStockProductsView.as_view()),
]