from rest_framework.views import APIView
from rest_framework.response import Response
from nitro_shop.apps.accounts.api.permissions import IsNotAuthenticated
from nitro_shop.apps.services.calculate import amount_information


class DiscountCalculationViews(APIView):
    """
    APIView for calculate discoint
    """
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        """return dict of  
        {
        "user_id": user_id,
        "items": items,
        "subtotal": subtotal,
        "cart_discount_amount": cart_discount_amount,
        "final_amount": final_amount,
        "status": "pending"
        }
        """
        data = amount_information()
        return Response(data)
