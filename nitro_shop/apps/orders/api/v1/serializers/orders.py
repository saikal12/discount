from rest_framework import serializers
from nitro_shop.apps.orders.models.orders import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializing items of order.
    Using in OrderSerializer."""
    product_text = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        model = OrderItem
        fields = ['product_text', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    """Serializing Order"""
    items = OrderItemSerializer(many=True)
    order_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Order
        fields = ['user_id', 'items', 'subtotal', 'discount_amount',
                  'final_amount', 'status', 'order_id']


class UserOrderSerializer(serializers.ModelSerializer):
    """Serializing users order"""
    order_id = serializers.IntegerField(
        source='id', read_only=True
    )
    created_at = serializers.DateTimeField(
        source='created_date', format='%Y-%m-%dT%H:%M:%S', read_only=True
    )

    class Meta:
        model = Order
        fields = ['order_id', 'created_at', 'subtotal',
                  'discount_amount', 'final_amount']

