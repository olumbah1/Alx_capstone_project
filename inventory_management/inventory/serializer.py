from rest_framework import serializers
from .models import StockMovement

class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ['id','user','movement_type','created_at','reason','quantity']
        read_only_fields = ['id','created_at']
        
        def validate_quantity(self,value):
            if value < 0:
                raise serializers.ValidationError("Quantity must be positive.")
            return value
        
        def validate_movement_type(self,value):
            if value not in ['IN', 'OUT']:
                raise serializers.ValidationError("Must be 'IN' or 'OUT'")
            return value
        
        def validate(self,data):
            # Check if removing more stock than available
            if data['movement_type'] == 'OUT':
                product = data['product']
                if product.current_stock < data['quantity']:
                    raise serializers.ValidationError("Not Enough stock available.")
            return data
                
            