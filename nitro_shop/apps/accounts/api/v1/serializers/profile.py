from rest_framework import serializers
from nitro_shop.apps.accounts.models.profile import Profile


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

