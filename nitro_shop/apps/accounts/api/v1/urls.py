from django.urls import path
from .views.crud_user import (
    RegisterView, UserUpdateView, UserDeleteView)
from .views.login import LoginView, LogoutView
from .views.password import ChangePasword
from .views.profile import UserProfileViews
from nitro_shop.apps.accounts.services.verification import (
    send_verification_change_password, verify_email)
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)
from nitro_shop.apps.orders.api.v1.views.orders import OrderHistoryViews


urlpatterns = [
    # User registration
    path('/',
         RegisterView.as_view(), name='register'),  

    # User profile
    path('<int:user_id>/',
         UserProfileViews.as_view(), name='profile'),

    # User update
    path('<int:user_id>/update/',
         UserUpdateView.as_view(), name='user_update'),

    # User delete
    path('/<int:user_id>/delete/',
         UserDeleteView.as_view(), name='user_delete'),

    # Email confirmation (verification)
    path('/verify-email/<str:uidb64>/<str:token>/',
         verify_email, name='verify_email'),

    # Request to change password (sends email with link)
    path('password-reset/',
         send_verification_change_password, name='password_change_request'),

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
