from rest_framework.response import Response
from nitro_shop.apps.discounts.api.v1.serializers.calculate_discounts import DiscountCalculationSerializer
from nitro_shop.apps.discounts.models.discount import DiscountRule
from nitro_shop.apps.accounts.models.profile import Profile
from rest_framework import status
from decimal import Decimal


def amount_information(request):
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
    8.return dict
    """
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
    return {
        "user_id": user_id,
        "items": items,
        "subtotal": subtotal,
        "cart_discount_amount": cart_discount_amount,
        "final_amount": final_amount,
        "status": "pending"
    }


def serializing_and_get_data(request):
    """Serializing and get user_id, items"""
    serializer = DiscountCalculationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    user_id = validated_data.get('user_id')
    items = validated_data.get('items', [])
    return user_id, items


def calculate_subtotal(items):
    """
    calculate_subtotal
    1. Get every cart_item
    2. multiply price and quantity
    3. Get sum of all cart_items.
    """
    return sum(Decimal(item['quantity']) * item['price'] for item in items)


def get_profile(user_id):
    """Get Profile objects with user_id"""
    try:
        profile = Profile.objects.get(user=user_id)
        return profile
    except Profile.DoesNotExist:
        return Response(
            {"error": "User profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )


def apply_cart_discount(subtotal):
    """
    Applying a discount to the shopping cart:
    1. Looking for the first suitable discount according to the rules.
    2. Calculates the discount amount based
    on the type (percentage or fixed).
    3. Limits the discount amount to the maximum value (if specified).
    4. Returns the dictionary with a discount and
    the new value of the basket after the discount.
    """
    discount_applieble = DiscountRule.objects.filter(
        min_order_value__lte=subtotal
    ).order_by('-min_order_value').first()
    if discount_applieble:
        if discount_applieble.discount_type == 'percentage':
            discoint_value = subtotal * (
                discount_applieble.discount_value / Decimal(100)
            )
        elif discount_applieble.discount_type == 'fixed':
            discoint_value = discount_applieble.discount_value
        discoint_value = min(discoint_value, discount_applieble.maximum_discount)
    cart_discounts_dict = {
        "type": "Cart Discount",
        "amount": discoint_value
    }
    cart_discounts_value = subtotal - discoint_value
    return cart_discounts_dict, cart_discounts_value


def apply_loyalty_discount(profile, subtotal):
    """
    Application of the discount under the loyalty program:
    1. Receives a user discount based on their profile.
    2. Calculates the discount percentage from the current cost.
    3. Returns the dictionary with a discount
    and the new value after the discount.
    """
    loyalty_discount = profile.get_loyalty_discount
    if loyalty_discount:
        loyal_discount_value = subtotal * (
            loyalty_discount.discount_percentage / Decimal(100)
        )
    loyalty_discount_dict = {
        "type": "Loyalty Discount",
        "amount": loyal_discount_value
    }
    amount_after_discount = subtotal - loyal_discount_value 
    return loyalty_discount_dict, amount_after_discount
