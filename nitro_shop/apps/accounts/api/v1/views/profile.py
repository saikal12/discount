from rest_framework.views import APIView
from rest_framework.response import Response
from nitro_shop.apps.accounts.models.profile import Profile
from ..serializers.profile import ProfileSerializer
from rest_framework.permissions import IsAuthenticated


class UserProfileViews(APIView):
    """Get Profile object from user_id.
    And serializing data.
    Returns a response with profile data"""
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        profile = Profile.objects.get(user=user_id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

