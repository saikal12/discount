from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


api_v1_urlpatterns = [
    path(
        'api/v1/users',
        include('nitro_shop.apps.accounts.api.v1.urls')),
    path(
        'api/v1/cart',
        include('nitro_shop.apps.discounts.api.v1.urls')
        ),
    path(
        'v1/logs/',
        include('nitro_shop.apps.logs.api.v1.urls')
    ),
    path('v1/orders', include('nitro_shop.apps.orders.api.v1.urls'))
]


schema_view = get_schema_view(
   openapi.Info(
      title="Calculation Discount API",
      default_version='v1',
      description="documentation for apps calculate_discount, discount project",
      # terms_of_service="URL страницы с пользовательским соглашением",
      contact=openapi.Contact(email="admin@kittygram.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    *api_v1_urlpatterns
]