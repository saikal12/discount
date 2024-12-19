from rest_framework.views import APIView
from rest_framework.response import Response
from nitro_shop.apps.accounts.services.verification import send_verification_email
from rest_framework import status
from nitro_shop.apps.accounts.api.permissions import IsNotAuthenticated, ReadOnly, Owner
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterView(APIView):
    """New user registration"""
    # Only non-authenticated users can access this view
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        # Getting the email and password from the request data
        email = request.data.get('email')
        password = request.data.get('password')
        # Checking if both email and password are provided
        if not email or not password:
            return Response({"error": "Email and password are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "A user with this email already exists."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create the user using the provided data
        user = User.objects.create_user(email=email, password=password)
        # Send a verification email after creating the user
        send_verification_email(user)

        return Response(
            {"message": "User created successfully. Please verify your email."},
            status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    # Permission class for read-only access to user details
    permission_classes = [ReadOnly]

    def get(self, request, user_id):
        try:
            # Try to retrieve the user by ID
            user = User.objects.get(id=user_id)
            return Response({"email": user.email, "username": user.username},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)


class UserUpdateView(APIView):
    # Permission class to ensure only the user owner can update
    permission_classes = [Owner]
    
    def put(self, request, user_id):
        try:
            # Try to retrieve the user by ID
            user = User.objects.get(id=user_id)
            user.email = request.data.get('email', user.email)
            # Update the user's email or username based on the request data
            user.username = request.data.get('username', user.username)
            user.save()
            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class UserDeleteView(APIView):
    # Permission class to ensure only the user owner can delete
    permission_classes = [Owner]

    def delete(self, request, user_id):
        try:
            # Try to retrieve the user by ID
            user = User.objects.get(id=user_id)

            user.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
