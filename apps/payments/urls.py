from django.urls import path

from apps.payments.views import SyncGatewayView, PaymentView

urlpatterns = [
    path('sync-gateways/', SyncGatewayView.as_view(), name='sync-gateways'),
    path('payment/done/', PaymentView.as_view(), name='payment-done'),
]

