from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)  # Current stock
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    low_stock_threshold = models.PositiveIntegerField(default=5)  # Alert when stock is low
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_products',
        help_text="User who created this product")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    
    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold # Check if product stock is below threshold

    @property
    def total_value(self):
        return self.price * self.quantity #  Calculate total value of current stock

    @property
    def creator_name(self): # Get the name of who created this product
        return f"{self.created_by.first_name} {self.created_by.last_name}".strip() or self.created_by.username