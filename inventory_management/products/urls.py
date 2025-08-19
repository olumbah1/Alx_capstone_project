from django.urls import path
from .views import ProductListCreateView, ProductDetailView, CategoryListCreateView, CategoryDetailView

urlpatterns = [
    path('', ProductListCreateView.as_view(), name = 'product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name = 'product-detail'),
    path('categories/', CategoryListCreateView.as_view(), name = 'categories'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name = 'category-detail')
]