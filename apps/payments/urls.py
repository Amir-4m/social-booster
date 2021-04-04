from django.urls import path

from apps.payments.views import SyncGatewayView

urlpatterns = [
    path('sync-gateways/', SyncGatewayView.as_view(), name='sync-gateways'),
]

