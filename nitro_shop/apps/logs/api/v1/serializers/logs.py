from rest_framework import serializers
from nitro_shop.apps.logs.models.logs import SystemLog


class SystemLogSerializer(serializers.ModelSerializer):
    """Serializing System Log"""
    class Meta:
        model = SystemLog
        fields = ['log_id', 'user_id', 'action_type', 'details', 'created_at']
        extra_kwargs = {
            'log_id': {'source': 'id', 'read_only': True},
            'created_at': {'format': '%Y-%m-%dT%H:%M:%S'}
        }
