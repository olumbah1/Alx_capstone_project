from django.urls import path
from .views import ProductListCreateView, ProductDetailView, CategoryListCreateView, CategoryDetailView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name = 'product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name = 'product-detail'),
    path('category/', CategoryListCreateView.as_view(), name = 'category-list'),
    path('category/<int:pk/', CategoryDetailView.as_view(), name = 'category-detail')
]