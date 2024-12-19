from rest_framework import serializers
from nitro_shop.apps.orders.api.v1.serializers.orders import OrderItemSerializer


class DiscountCalculationSerializer(serializers.Serializer):
    """Serializing discount cart"""
    user_id = serializers.IntegerField()
    items = OrderItemSerializer(many=True)