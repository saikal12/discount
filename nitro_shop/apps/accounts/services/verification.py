from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

import logging


logger = logging.getLogger(__name__)


def decode_and_check_token(request, uidb64, token):
    try:
        # Decoded user ID
        uid = urlsafe_base64_decode(uidb64).decode()
        # Get user by ID
        user = get_object_or_404(User, pk=uid)
        logger.info(f"User found: {user.email}, UID: {uid}")
    except Exception as e:
        logger.error(f"Error decoding token: {str(e)}")
        return None, str(e)
        # Check the token
    if not default_token_generator.check_token(user, token):
        logger.error(f"Invalid token for user: {user.email}")
        return None, "Invalid token"
    return user, None


def verify_email(request, uidb64, token):
    user, error = decode_and_check_token(request, uidb64, token) 
    if error:
        return JsonResponse({"error": error}, status=400)
    user.is_email_verified = True
    user.save()
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return JsonResponse({
        "message": "Email verified successfully",
        "access_token": access_token,
        "refresh_token": str(refresh),
    }, status=200)


def make_token_uid(user):
    """generate token, encode user
    return token and uid """
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    return token, uid


def send_verification_email(user):
    token, uid = make_token_uid(user)
    verification_link = f"{settings.API_URL}/users/verify-email/{uid}/{token}/"
    subject = "Email Verification"
    message = f"Hi {user.username},\nPlease verify your email by sending a request to the following link:\n{verification_link}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
    logger.info(f"email sending for {user.email}")
    return
