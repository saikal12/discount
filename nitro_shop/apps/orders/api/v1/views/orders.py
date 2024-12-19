from rest_framework.response import Response
from nitro_shop.apps.orders.api.v1.serializers.orders import OrderSerializer, UserOrderSerializer
from nitro_shop.apps.orders.models.orders import Order, OrderItem
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from nitro_shop.apps.services.calculate import amount_information
from nitro_shop.apps.accounts.api.permissions import OwnerOrReadOnly, ReadOnly


class OrdersManagementViews(viewsets.ModelViewSet):
    """Includes actions like
    list, create, retrieve, update, partial_update, destroy"""
    permission_classes = [OwnerOrReadOnly]
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
    permission_classes = [ReadOnly]
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
            "total": len(serializer.data),
            "page": self.request.query_params.get('page', 1)
        }, status=status.HTTP_200_OK)
