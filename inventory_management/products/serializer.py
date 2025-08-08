from rest_framework import serializers
from .models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','price','category','description','current_stock','minimum_stock','created_at']
        read_only_fields = ['id','created_at']
        
        def validate_price(self,value):
            if value <= 0:
                raise serializers.ValidationError("Price must be greater than zero.")
            return value
        
        def validate_current_stock(self,value):
            if value < 0:
                raise serializers.ValidationError("Current stock cannot be negative.")
            return value
            
        def validate_minimum_stock(self,value):
            if value < 0:
                raise serializers.ValidationError("Minimum stock cannnot be negative.")
            return value
        
        def validate(self,data):
            current_stock = data.get('current_stock')
            minimum_stock = data.get('minimum_stock')
            
    # Make sure current stock is not less than minimum stock if both are provided
            if current_stock is not None and minimum_stock is not None:
                if current_stock < minimum_stock:
                    raise serializers.ValidationError(
                    "Current stock cannot be less than minimum stock."
                   )
            return data
        
               
class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products']
        
