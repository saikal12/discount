from rest_framework import serializers
from .models import Profile, Order, OrderItem, SystemLog


class ProfileSerializer(serializers.Serializer):
    """Serializing Profile.
    Some fields are taken from the user"""
    user_id = serializers.IntegerField(
        source='user.id', read_only=True
        )
    email = serializers.EmailField(
        source='user.email', read_only=True
        )
    created_at = serializers.DateTimeField(
        source='user.date_joined', read_only=True, format='%Y-%m-%dT%H:%M:%S'
    )
    orders_count = serializers.IntegerField()
    total_spent = serializers.DecimalField(max_digits=10, decimal_places=2)
    loyalty_status = serializers.CharField()
    tier = serializers.CharField()

    class Meta:
        model = Profile
        field = ['user_id', 'email', 'created_at', 'orders_count',
                 'total_spent', 'loyalty_status', 'tier']


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

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        if not items_data:
            raise serializers.ValidationError(
                {'items': 'Order must contain at least one item.'}
            )
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order_id=order, **item_data)
        return order
# add update for Put


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


class DiscountCalculationSerializer(serializers.Serializer):
    """Serializing discount cart"""
    user_id = serializers.IntegerField()
    items = OrderItemSerializer(many=True)


class SystemLogSerializer(serializers.ModelSerializer):
    """Serializing System Log"""
    class Meta:
        model = SystemLog
        fields = ['log_id', 'user_id', 'action_type', 'details', 'created_at']
        extra_kwargs = {
            'log_id': {'source': 'id', 'read_only': True},
            'created_at': {'format': '%Y-%m-%dT%H:%M:%S'}
        }
