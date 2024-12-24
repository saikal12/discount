from rest_framework.views import APIView
from rest_framework.response import Response
from nitro_shop.apps.accounts.services.verification import send_verification_email
from rest_framework import status
from nitro_shop.apps.accounts.api.permissions import IsNotAuthenticated, ReadOnly, Owner
from django.contrib.auth import get_user_model

import logging


logger = logging.getLogger(__name__)

User = get_user_model()


class RegisterView(APIView):
    """New user registration"""
    # Only non-authenticated users can access this view
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        # Getting the email and password from the request data
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')
        # Checking if both email and password are provided
        if not email or not password or not username:
            return Response({"error": "Email, password, username are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "A user with this email already exists."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            # Create the user using the provided data
            user = User.objects.create_user(email=email, password=password, username=username)
            logger.info("User created successfully.")
            # send verification email to user.email
            send_verification_email(user)
            logger.info("Email send successfully.")
            return Response(
                {"message": "User created successfully. Please verify your email."},
                status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Database operation failed: {str(e)}")
            return Response(
                {"error": "An error occurred during user creation."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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


class UserListView(APIView):
    # Permission class for read-only access
    permission_classes = [ReadOnly]

    def get(self, request):
        # Get all users
        users = User.objects.all().values('id', 'email', 'username')
        return Response(users, status=status.HTTP_200_OK)


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
