from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.orders.api.serializers import OrderSerializer
from apps.orders.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]
