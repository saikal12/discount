from django.urls import path
from nitro_shop.apps.discounts.api.v1.views.calculate_discounts import DiscountCalculationViews

urlpatterns = [
    path('calculate-discount/',
         DiscountCalculationViews.as_view(), name='calculate_discount'),
]