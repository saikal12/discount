from django.contrib import admin
from .models.discount import LoyaltyDiscount, DiscountRule


@admin.register(LoyaltyDiscount)
class LoyaltyDiscountAdmin(admin.ModelAdmin):
    list_display = (
        'level_name', 'min_order', 'max_order', 'discount_percentage'
        )
    list_filter = ('level_name',)
    search_fields = ('level_name', 'discount_percentage')
    ordering = ['min_order']


@admin.register(DiscountRule)
class DiscountRuleAdmin(admin.ModelAdmin):
    list_display = ('description', 'discount_type',
                    'maximum_discount', 'discount_value', 'min_order_value')
    list_filter = ('discount_type',)
    search_fields = ('description', 'discount_type')
    ordering = ['min_order_value']
