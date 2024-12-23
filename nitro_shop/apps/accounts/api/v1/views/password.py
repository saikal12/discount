from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from nitro_shop.apps.accounts.services.verification  import decode_and_check_token
from rest_framework.permissions import IsAuthenticated


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