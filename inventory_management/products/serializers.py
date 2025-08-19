from rest_framework import serializers
from .models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
     # These fields show user info in API responses
    creator_name = serializers.ReadOnlyField()  # Uses the property from model
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    
    class Meta:
        model = Product
        fields = [
            'id', 
            'name', 
            'price', 
            'category', 
            'description', 
            'quantity', 
            'low_stock_threshold', 
            'created_by',           # User ID (will be set automatically)
            'creator_name',         # Full name or username
            'created_by_username',  # Just the username
            'created_at', 
            'updated_at'
        ]
        read_only_fields = [
            'id', 
            'created_by',           # User can't manually set this
            'creator_name',
            'created_by_username', 
            'created_at', 
            'updated_at'
        ]
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
    
    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value
        
    def validate_low_stock_threshold(self, value):
        if value < 0:
            raise serializers.ValidationError("Low stock threshold cannot be negative.")
        return value
    
    def validate(self, data):
        quantity = data.get('quantity')
        low_stock_threshold = data.get('low_stock_threshold')
        
        if quantity is not None and low_stock_threshold is not None:
            if quantity < low_stock_threshold:
                raise serializers.ValidationError(
                    "Current quantity cannot be less than low stock threshold."
                )
        return data

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products']