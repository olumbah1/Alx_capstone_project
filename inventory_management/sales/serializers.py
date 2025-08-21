from rest_framework import serializers
from .models import Customer, Sale, SaleItem

# CUSTOMER SERIALIZER
class CustomerSerializer(serializers.ModelSerializer):
    total_purchases = serializers.SerializerMethodField()
    total_spent = serializers.SerializerMethodField()
    
    class Meta:
        model = Customer
        fields = '__all__'
    
    def get_total_purchases(self, obj):
        return obj.sale_set.count()
    
    def get_total_spent(self, obj):
        total = sum(sale.total_amount for sale in obj.sale_set.all())
        return float(total)

# SALE ITEM SERIALIZER - Shows product details
class SaleItemSerializer(serializers.ModelSerializer):
    # Show product information
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_category = serializers.CharField(source='product.category.name', read_only=True)
    catalog_price = serializers.DecimalField(
        source='product.price', 
        read_only=True, 
        max_digits=10, 
        decimal_places=2
    )
    available_stock = serializers.IntegerField(source='product.quantity', read_only=True)
    
    class Meta:
        model = SaleItem
        fields = [
            'id', 'product', 'product_name', 'product_category',
            'catalog_price', 'available_stock', 'quantity', 
            'unit_price', 'total_price'
        ]
        read_only_fields = ('total_price',)
    
    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity', 0)
        
        # CHECK STOCK AVAILABILITY
        if product and quantity > product.quantity:
            raise serializers.ValidationError(
                f"Not enough stock! Available: {product.quantity}, Requested: {quantity}"
            )
        
        # AUTO-FILL unit_price if not provided
        if 'unit_price' not in data or data['unit_price'] is None:
            if product:
                data['unit_price'] = product.price
        
        return data

# SALE SERIALIZER
class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    items_count = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Sale
        fields = '__all__'
    
    def get_items_count(self, obj):
        return obj.items.count()
    
    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

# SALE CREATE SERIALIZER
class SaleCreateSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)
    
    class Meta:
        model = Sale
        fields = ['customer', 'notes', 'items']
    
    def validate_items(self, items_data):
        """Validate all items before creating sale"""
        if not items_data:
            raise serializers.ValidationError("At least one item is required")
        
        # Check stock for all items
        for item_data in items_data:
            product = item_data.get('product')
            quantity = item_data.get('quantity', 0)
            
            if product and quantity > product.quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for {product.name}! Available: {product.quantity}, Requested: {quantity}"
                )
        
        return items_data
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        sale = Sale.objects.create(**validated_data)
        
        # Create items (this will automatically reduce stock)
        for item_data in items_data:
            SaleItem.objects.create(sale=sale, **item_data)
        
        return sale