from django.db import models


class DiscountRule(models.Model):
    """
    The rules of the discount that the admin assigns through the admin zone.
    Includes description, type, maximum_discount,
    discount_value, min_order_value
    """

    description = models.TextField()
    discount_type = models.CharField(
        max_length=50, choices=[
            ('percentage', 'Percentage'), ('fixed', 'Fixed')
            ]
        )  # Type in percentage, fixed
    maximum_discount = models.DecimalField(
        max_digits=10, decimal_places=2
        )    # for example, the discount cannot be more than 50$
    discount_value = models.DecimalField(
        max_digits=10, decimal_places=2
        )    # Discount value
    min_order_value = models.DecimalField(
        max_digits=10, decimal_places=2
        )   # for example, order>min_order_value


class LoyaltyDiscount(models.Model):
    """
    Through the admin zone, it sets up how many orders
    need to be made to get a certain level.
    And adjusts the discount percentages for each level"""

    level_name = models.CharField(max_length=50, unique=True)
    min_order = models.IntegerField()
    max_order = models.IntegerField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ['min_order']

    def __str__(self):
        return f"{self.level_name}: {self.discount_percentage}%"
