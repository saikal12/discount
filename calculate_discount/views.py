from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    ProfileSerializer, OrderSerializer,
    UserOrderSerializer, DiscountCalculationSerializer, SystemLogSerializer
)
from .models import Profile, DiscountRule, Order, SystemLog, OrderItem
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, viewsets
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from decimal import Decimal
from rest_framework.exceptions import NotFound
from .utils import amount_information


class DiscountCalculationViews(APIView):
    """
    APIView for calculate discoint
    """
    def post(self, request):
        """return dict of  
        {
        "user_id": user_id,
        "items": items,
        "subtotal": subtotal,
        "cart_discount_amount": cart_discount_amount,
        "final_amount": final_amount,
        "status": "pending"
        }
        """
        data = amount_information()
        return Response(data)


class UserProfileViews(APIView):
    """Get Profile object from user_id.
    And serializing data.
    Returns a response with profile data"""
    def get(self, request, user_id):
        profile = Profile.objects.get(user=user_id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class OrdersManagementViews(viewsets.ModelViewSet):
    """Includes actions like
    list, create, retrieve, update, partial_update, destroy"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request):
        data = amount_information(request)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        data = amount_information(request)
        order.subtotal = data['subtotal']
        order.discount_amount = data['cart_discount_amount']
        order.final_amount = data['final_amount']
        order.status = data["status"]
        order.save()
        order.items.all().delete()
        for item in data['items']:
            OrderItem.objects.create(order_id=order, **item)
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderHistoryViews(ListAPIView):
    serializer_class = UserOrderSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if not user_id:
            raise NotFound(detail="User ID is required.")
        return Order.objects.filter(user_id=user_id).order_by('-created_date')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "orders": serializer.data,
            "total": len(serializer.data),  # Общее количество заказов
            "page": self.request.query_params.get('page', 1)
        }, status=status.HTTP_200_OK)


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
        fields = ['user_id', 'action_type', 'created_at', 'from_date', 'from_date']


class SystemLogsViews(ListAPIView):
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