from django.apps import AppConfig


class CalculateDiscountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nitro_shop.apps.discounts'

    def ready(self):
        from . import signals