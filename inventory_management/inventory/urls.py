from django.urls import path
from .views import (StockMovementListCreateView, 
                    StockMovementDetailView,
                    InventorySummaryView, 
                    LowStockProductsView)

urlpatterns = [
    path('movements/', StockMovementListCreateView.as_view(), name = 'movement-list'),
    path('movements/<int:pk>/', StockMovementDetailView.as_view(), name = 'movement-detail'),
    path('summary/', InventorySummaryView.as_view(), name = 'inventory-summary'),
    path('low-stock/', LowStockProductsView.as_view(), name = 'low-stock'),
    
]
