from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.
class StockMovement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=100)
    quantity = models.IntegerField()
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='movement_created_by')
    
    def __str__(self):
        return f"{self.movement_type} - {self.product.name} ({self.quantity})" # Shows movement type, product and quantity