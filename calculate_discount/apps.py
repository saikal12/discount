from django.apps import AppConfig

class CalculateDiscountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calculate_discount'

    def ready(self):
        import calculate_discount.signals