from django.urls import path, include
from nitro_shop.apps.orders.api.v1.views.orders import OrdersManagementViews
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'orders', OrdersManagementViews)

urlpatterns = [
    path('/', include(router.urls))]