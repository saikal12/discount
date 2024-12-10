from django.urls import path, include
from .views import (
    DiscountCalculationViews, UserProfileViews,
    OrdersManagementViews, OrderHistoryViews, SystemLogsViews
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'orders', OrdersManagementViews)

urlpatterns = [
    path(
        'v1/users/<int:user_id>/',
        UserProfileViews.as_view(), name='profile'
         ),
    path(
        'v1/cart/calculate-discount/',
        DiscountCalculationViews.as_view(), name='calculate_discount'
         ),
    path(
        'v1/users/<int:user_id>/orders/',
        OrderHistoryViews.as_view(), name='order_history'
         ),
    path(
        'v1/logs/',
        SystemLogsViews.as_view(), name='system_log'
    ),
    path('v1/', include(router.urls))

]
