from django.contrib import admin
from .models import Customer, Sale, SaleItem

# Register your models here.


# Register Customer model
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']  # Show these columns
    search_fields = ['name', 'email']  # Can search by these

# Inline for adding sale items when creating a sale
class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1  # Show 1 empty form
    readonly_fields = ('total_price',)  # Can't edit this (auto-calculated)

# Register Sale model with inline items
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['sale_number', 'customer', 'total_amount', 'payment_status', 'sale_date']
    list_filter = ['payment_status', 'sale_date']  # Add filters
    search_fields = ['sale_number', 'customer__name']
    readonly_fields = ['sale_number', 'total_amount']  # Auto-generated fields
    inlines = [SaleItemInline]  # Add items inline