from django.urls import path
from nitro_shop.apps.logs.api.v1.views.logs import SystemLogsViews


urlpatterns = [
    path('logs/',  SystemLogsViews.as_view(), name='system_log')
]