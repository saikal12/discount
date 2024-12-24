from django.urls import path
from .views.crud_user import (
    RegisterView, UserUpdateView, UserDeleteView, UserListView, UserDetailView)
from .views.login import LoginView, LogoutView
from .views.password import ChangePasword, ResetPasword
from .views.profile import UserProfileViews
from nitro_shop.apps.accounts.services.verification import verify_email
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)
from nitro_shop.apps.orders.api.v1.views.orders import OrderHistoryViews
from django.http import JsonResponse


def debug_view(request, *args, **kwargs):
    return JsonResponse({"debug": "Route is working", "args": kwargs})

urlpatterns = [
    # User registration
    path('',
         RegisterView.as_view(), name='register'),
    # User profile
    path('<int:user_id>/',
         UserProfileViews.as_view(), name='profile'),
    #  Users list 
    path('list/', UserListView.as_view(), name='user_list'),
    # User Detail
    path('<int:user_id>/detail/', UserDetailView.as_view(), name='user_detail'),
    #path('<int:user_id>/detail/', debug_view, name='debug_user_detail'),
    # User update
    path('<int:user_id>/update/',
         UserUpdateView.as_view(), name='user_update'),

    # User delete
    path('<int:user_id>/delete/',
         UserDeleteView.as_view(), name='user_delete'),

    # Email confirmation (verification)
    path('verify-email/<str:uidb64>/<str:token>/',
         verify_email, name='verify_email'),

    # Request to change password (sends email with link)
    path('password_reset/',
         ResetPasword.as_view(), name='password_change_request'),

    # Confirm password change
    path('reset_password/<str:uidb64>/<str:token>/',
         ChangePasword.as_view(), name='password_reset_confirm'),
    # User login
    path('login', LoginView.as_view(), name='login'),
    # User logout
    path('logout', LogoutView.as_view(), name='logout'),
    # Token management (JWT)
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # User orders history
    path('<int:user_id>/orders',
         OrderHistoryViews.as_view(), name='order_history')

]
