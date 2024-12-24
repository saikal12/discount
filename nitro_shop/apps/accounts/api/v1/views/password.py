from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from nitro_shop.apps.accounts.services.verification  import decode_and_check_token, make_token_uid, send_mail
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import status

User = get_user_model()


class ResetPasword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Extract email from the request body
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        # Generate token and UID
        token, uid = make_token_uid(user)
        verification_link = f"{settings.API_URL}/api/verify-email/{uid}/{token}/"
        subject = "Email Verification"
        message = f"Hi {user.username},\nPlease verify your email by sending a request to the following link:\n{verification_link}"
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
        except Exception as e:
            return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message": "Password reset email sent successfully."}, status=status.HTTP_200_OK)


class ChangePasword(APIView):
    permission_classes = [IsAuthenticated]

    def post(request, uid, token):
        # Decode the token and validate the user
        user, error = decode_and_check_token(request, uid, token)
        if error:
            # Return an error if the token is invalid or the user is not found
            return JsonResponse({"error": error}, status=400)
        # Retrieve the new password from the request data
        new_password = request.data.get("password")
        if not new_password:
            # Return an error if the password is not provided
            return JsonResponse({"error": "Password is required"}, status=400)
        try:
            # Validate the new password against password policy rules
            validate_password(new_password, user)
        except ValidationError as e:
            # Return validation errors if the password does not meet the requirements
            return JsonResponse({"error": e.messages}, status=400)
        # Set the new password for the user
        user.set_password(new_password)
        # Save the updated user object
        user.save()
        # Return a success message
        return JsonResponse({"message": "Password reset successful"}, status=200)