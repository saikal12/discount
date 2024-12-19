from django.db import models
from django.db.models import Q
from nitro_shop.apps.discounts.models.discount import LoyaltyDiscount
from django.conf import settings


class Profile(models.Model):
    """The profile of the user whose fields
    are calculated dynamically.
    Includes user, orders_count, total_spent,
    get_loyality_discount, loyality_status, tier"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def orders_count(self):
        return self.user.order.count()

    @property
    def total_spent(self):
        all_order = self.user.order.all()
        return sum(order.final_amount for order in all_order)

    @property
    def get_loyalty_discount(self):
        order_count = self.orders_count
        discount = LoyaltyDiscount.objects.filter(
            Q(min_order__lte=order_count) &
            Q(max_order__gte=order_count)
        ).first()
        return discount

    @property
    def loyalty_status(self):
        discount = self.get_loyalty_discount
        return discount.level_name if discount else "Basic"

    @property
    def tier(self):
        discount = self.get_loyalty_discount
        return f"{discount.discount_percentage}%" if discount else "0%"
