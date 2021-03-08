from django.urls import path
from rest_framework import routers

from apps.orders.api.views import OrderViewSet, OrderGateWayAPIView, GatewayAPIView, PurchaseVerificationAPIView

router = routers.SimpleRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('order-gateway/', OrderGateWayAPIView.as_view(), name='order-gateway'),
    path('gateways/', GatewayAPIView.as_view(), name='gateways-list'),
    path('purchase-verification/', PurchaseVerificationAPIView.as_view(), name='purchase-verification'),
]
urlpatterns += router.urls

