import json
import stripe

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import api_view

from .models import Order
from .serializers import OrderSerializer


pk = stripe.api_key = "sk_test_51IEbV8Ezf3A4EKZT7lNhU29B1D1SYxzGs7XfysrlcswQtfjiEuItidMlWTCa7uw3AxiTmyfJbvVR0uEVsAvv6Xux007ZTBD96E"


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet
                   ):
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Order.objects.filter(user=user)


@api_view(['POST'])
def create_payment_intent(request, order_id):
    try:
        order_instance = Order.objects.get(id=order_id)
        order_in_total = int(order_instance.total * 100)
        order_instance.status = 'in_delivery'
        order_instance.save()
        intent = stripe.Charge.create(
            amount=request.POST.get('amount', order_in_total),
            currency=request.POST.get('currency', 'USD'),
            source=request.POST.get('source', ''),
            description=request.POST.get('description', ''),
            metadata={'order_id': 12345},
        )
        content = json.dumps({'client_secret': intent['client_secret']})

        return HttpResponse(json.dumps(
            {'message': 'Your transaction has been successful.'})
        )
    except Exception:
        return HttpResponse(json.dumps(
            {'message': 'Your transaction has been successful.'})
        )
