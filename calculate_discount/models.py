from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from decimal import Decimal


class Profile(models.Model):
    """The profile of the user whose fields
    are calculated dynamically.
    Includes user, orders_count, total_spent,
    get_loyality_discount, loyality_status, tier"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),           # Заказ создан, ожидает обработки
        ('processing', 'Processing'),     # Заказ в обработке
        ('completed', 'Completed'),       # Заказ завершён
        ('cancelled', 'Cancelled'),       # Заказ отменён
    ]
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='order'
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    final_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    created_date = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order_id = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='items'
    )
    product_text = models.CharField(max_length=255)
    quantity = models.IntegerField(max_length=10)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
    )


class DiscountRule(models.Model):
    """
    The rules of the discount that the admin assigns through the admin zone.
    Includes description, type, maximum_discount,
    discount_value, min_order_value"""
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


class SystemLog(models.Model):
    """A model for recording logs
    like login, logout create, update, delete"""
    ACTION_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='systemlog')
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    details = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)


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
