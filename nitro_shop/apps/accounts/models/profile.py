from django.db import models
from django.db.models import Q
from nitro_shop.apps.discounts.models.discount import LoyaltyDiscount
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    """The profile of the user whose fields
    are calculated dynamically.
    Includes user, orders_count, total_spent,
    get_loyality_discount, loyality_status, tier"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def orders_count(self):
        # Returns the count of orders the user has placed
        return self.user.order.count()

    @property
    def total_spent(self):
        # Calculates the total amount the user has spent based on all their orders
        all_order = self.user.order.all() # Get all the orders of the user
        return sum(order.final_amount for order in all_order)

    @property
    def get_loyalty_discount(self):
        # Gets the applicable loyalty discount for the user based on the count of orders
        order_count = self.orders_count
        # Find the discount where the user's order count is between the min and max order limits
        discount = LoyaltyDiscount.objects.filter(
            Q(min_order__lte=order_count) &  # Minimum orders condition
            Q(max_order__gte=order_count)  # Maximum orders condition
        ).first()  # Get the first matching discount
        return discount  # Return the discount if found, otherwise None

    @property
    def loyalty_status(self):
        # Returns the loyalty status level for the user
        discount = self.get_loyalty_discount  # Get the applicable discount
        # Return the discount's level name, or "Basic" if no discount is found
        return discount.level_name if discount else "Basic"

    @property
    def tier(self):
        # Returns the user's loyalty tier (discount percentage)
        discount = self.get_loyalty_discount
        # Return the discount percentage as a string, or "0%" if no discount is found
        return f"{discount.discount_percentage}%" if discount else "0%"
