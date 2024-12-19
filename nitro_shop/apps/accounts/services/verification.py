from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


def decode_and_check_token(request, uidb64, token):
    try:
        # Декодируем id пользователя (получаем ID из URL)
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)  # Получаем пользователя по ID
    except Exception as e:
        return None, str(e)
        # Проверяем токен
    if not default_token_generator.check_token(user, token):
        return None, "Invalid token"


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
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    return token, uid


def send_verification_email(user):
    token, uid = make_token_uid(user)
    verification_link = f"{settings.API_URL}/api/verify-email/{uid}/{token}/"
    subject = "Email Verification"
    message = f"Hi {user.username},\nPlease verify your email by sending a request to the following link:\n{verification_link}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


def send_verification_change_password(user):
    token, uid = make_token_uid(user)
    reset_link = f"{settings.API_URL}/api/reset_password/{uid}/{token}/"
    subject = "Password Reset Request"
    message = f"Hi {user.username},\nClick the link below to reset your password:\n{reset_link}\n{reset_link}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])



