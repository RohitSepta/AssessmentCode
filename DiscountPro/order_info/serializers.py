from rest_framework import serializers
from .models import OrderItem, Order

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    subtotal = serializers.FloatField(source='get_subtotal', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_name', 'quantity',
            'unit_price', 'final_price', 'subtotal'
        ]
        read_only_fields = ['unit_price', 'final_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    savings = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'items',
            'total_amount', 'discounted_total', 'savings',
            'applied_discount', 'created_at', 'updated_at'
        ]
        read_only_fields = ['order_number', 'total_amount', 'discounted_total']

    def get_savings(self, obj):
        return float(obj.total_amount - obj.discounted_total)

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Generate unique order number (you might want to customize this)
        validated_data['order_number'] = f"ORD-{Order.objects.count() + 1:06d}"
        
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
            
        order.calculate_totals()
        return order