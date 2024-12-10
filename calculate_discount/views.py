from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    ProfileSerializer, OrderSerializer,
    UserOrderSerializer, DiscountCalculationSerializer
)
from .models import Profile, DiscountRule, Order, SystemLog
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, viewsets
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from decimal import Decimal
from rest_framework.exceptions import NotFound
from .utils import calculate_subtotal, apply_cart_discount, apply_loyalty_discount, get_profile, serializing_and_get_data


class DiscountCalculationViews(APIView):
    """
    APIView for calculate discoint
    """
    def post(self, request):
        """
        1.serializing and get data(user_id, items)
        2.calculate subtotal
        3.get profile object by user_id
        4.calculates which discount is more suitable and
        applies for subtotal
        5.calculates which loyality discount is more suitable and
        applies for amount after 4.point
        6.add discounts in dict
        7.final amount its amount after loyality discount
        8.return dict"""
        user_id, items = serializing_and_get_data(request)
        subtotal = calculate_subtotal(items)
        profile = get_profile(user_id)
        cart_discoint, cart_value = apply_cart_discount(subtotal)
        loyal_discount, loyal_value = apply_loyalty_discount(
            profile, cart_value
            )
        discounts = [cart_discoint, loyal_discount]
        final_amount = loyal_value
        discount_total = cart_discoint['amount'] + loyal_discount['amount']
        dict = {
            "subtotal": subtotal,
            "discounts": discounts,
            "total_discount": discount_total,
            "final_amount": final_amount
        }
        return Response(dict)




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
        user_id, items = serializing_and_get_data(request)
        subtotal = calculate_subtotal(items)
        profile = get_profile(user_id)
        cart_discoint, cart_value = apply_cart_discount(subtotal)
        loyal_discount, loyal_value = apply_loyalty_discount(
            profile, cart_value
            )
        discount_total = cart_discoint['amount'] + loyal_discount['amount']
        cart_discount_amount = Decimal(discount_total).quantize(Decimal('0.01'))
        final_amount = Decimal(loyal_value).quantize(Decimal('0.01'))
        data = {
            "user_id": user_id,
            "items": items, 
            "subtotal": subtotal,
            "discount_amount": cart_discount_amount,
            "final_amount": final_amount,
            "status": "pending"
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        field_name='user_id', lookup_expr='iexact'
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
        fields = ['user_id', 'action_type', 'created_at', 'from_date']


class SystemLogsViews(ListAPIView):
    serializer_class = UserOrderSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = SystemLogFilter

    def get_queryset(self):
        return SystemLog.objects.all().order_by('-created_at')