from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from nitro_shop.apps.accounts.services.verification  import decode_and_check_token
from rest_framework.permissions import IsAuthenticated


class ChangePasword(APIView):
    permission_classes = [IsAuthenticated]

    def post(request, uid, token):
        user, error = decode_and_check_token(request, uid, token)
        if error:
            return JsonResponse({"error": error}, status=400)
        new_password = request.data.get("password")
        if not new_password:
            return JsonResponse({"error": "Password is required"}, status=400)
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return JsonResponse({"error": e.messages}, status=400)
        # Устанавливаем новый пароль
        user.set_password(new_password)
        user.save()
        return JsonResponse({"message": "Password reset successful"}, status=200)