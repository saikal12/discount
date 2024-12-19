from rest_framework.response import Response
from nitro_shop.apps.logs.api.v1.serializers.logs import SystemLogSerializer
from nitro_shop.apps.logs.models.logs import SystemLog
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from nitro_shop.apps.accounts.api.permissions import IsAdmin


class SystemLogFilter(filters.FilterSet):
    user_id = filters.CharFilter(
        field_name='user_id', lookup_expr='exact'
    )
    action_type = filters.CharFilter(
        field_name='action_type', lookup_expr='iexact'
    )
    from_date = filters.DateTimeFilter(
        field_name='created_at', lookup_expr='gte'
    )
    to_date = filters.DateTimeFilter(
        field_name='created_at', lookup_expr='lte'
    )

    class Meta:
        model = SystemLog
        fields = ['user_id', 'action_type', 'created_at', 'from_date',]


class SystemLogsViews(ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = SystemLogSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = SystemLogFilter

    def get_queryset(self):
        return SystemLog.objects.all().order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        total = len(queryset)
        page_number = self.paginate_queryset(queryset).number if self.paginate_queryset(queryset) else 1
        return Response({
            'logs': serializer.data,
            'total': total,
            'page': page_number
        })
