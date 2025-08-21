from django.db import models
from django.contrib.auth.models import User
from products.models import Product
# Create your models here.

# CUSTOMER MODEL
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

# SALE MODEL
class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('pending', 'Not Paid Yet'),
        ('paid', 'Fully Paid'),
        ('partial', 'Partially Paid'),
    ]
    
    sale_number = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sale_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Auto-generate sale number like SALE001, SALE002
        if not self.sale_number:
            last_sale = Sale.objects.all().order_by('id').last()
            if last_sale:
                try:
                    last_number = int(last_sale.sale_number[4:])  # Get number after 'SALE'
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.sale_number = f'SALE{new_number:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sale_number} - {self.customer.name}"
    
    class Meta:
        ordering = ['-created_at']

# SALE ITEM MODEL - Links to your Product model
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Uses YOUR Product model
    quantity = models.PositiveIntegerField()
    # Auto-fills from product.price but can be overridden for discounts
    unit_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Price per unit (auto-fills from product price)"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # AUTO-FILL: If no unit_price provided, use product price
        if not self.unit_price and self.product:
            self.unit_price = self.product.price
            
        # Auto-calculate total price
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        
        # REDUCE STOCK: Update product quantity when sale is made
        if self.product:
            # Check if we have enough stock
            if self.product.quantity >= self.quantity:
                self.product.quantity -= self.quantity
                self.product.save()
            else:
                raise ValueError(f"Not enough stock! Available: {self.product.quantity}, Requested: {self.quantity}")
        
        # Update sale total
        self.update_sale_total()
    
    def update_sale_total(self):
        """Update the total amount of the sale"""
        sale = self.sale
        sale.total_amount = sum(item.total_price for item in sale.items.all())
        sale.save()
    
    def __str__(self):
        return f"{self.product.name} ({self.quantity}) - {self.sale.sale_number}"