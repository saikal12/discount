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
    # Only allows read-only or owner can access to this view
    permission_classes = [OwnerOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request):
        #return user_id, items subtotal , cart_discount_amount, final_amount , status
        data = amount_information(request) # Fetch amount and order details
        serializer = self.get_serializer(data=data) # Initialize the serializer with the data
        serializer.is_valid(raise_exception=True) # Validate the serializer data
        self.perform_create(serializer)  # Save the validated data to the database

        return Response(serializer.data, status=status.HTTP_201_CREATED) # Return the response with the saved data

    def update(self, request, *args, **kwargs):
        order = self.get_object() # Retrieve the order object to be updated
        data = amount_information(request) # Fetch the updated amount and order details
        order.subtotal = data['subtotal'] # Update the order subtotal
        order.discount_amount = data['cart_discount_amount'] # Update the cart_discount_amount
        order.final_amount = data['final_amount'] # status
        order.save()  # Save the updated order details to the database
        order.items.all().delete() # Remove all existing items from the order
        for item in data['items']: # Add new items to the order
            OrderItem.objects.create(order_id=order, **item) # Create and link items to the order
        serializer = self.get_serializer(order) # Serialize the updated order
        return Response(serializer.data, status=status.HTTP_200_OK) # Return the updated order details


class OrderHistoryViews(ListAPIView):
    # Only allows read-only access to this view
    permission_classes = [ReadOnly]
    serializer_class = UserOrderSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user_id = self.kwargs.get('user_id') # Extract user ID from the URL
        if not user_id:
            raise NotFound(detail="User ID is required.")
        return Order.objects.filter(user_id=user_id).order_by('-created_date') # Query and return user's orders

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset() # Fetch the filtered queryset
        page = self.paginate_queryset(queryset)  # Apply pagination to the queryset
        if page is not None:  # If the data is paginated
            serializer = self.get_serializer(page, many=True) # Serialize the paginated data
            return self.get_paginated_response(serializer.data)  # Return paginated response
        serializer = self.get_serializer(queryset, many=True) # Serialize the full queryset
        return Response({
            "orders": serializer.data, # Include serialized order data
            "total": len(serializer.data), # Include the total number of orders
            "page": self.request.query_params.get('page', 1) # Include the current page number
        }, status=status.HTTP_200_OK)  # Return the full response
