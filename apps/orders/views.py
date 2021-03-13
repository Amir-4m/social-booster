from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.orders.services import CustomService
from django.core.cache import cache


class SyncGatewayView(View):

    def get(self, request):
        # the gateways should be synced here
        if request.user.is_superuser:
            data = CustomService.payment_request('gateways', 'get')
            cache.set("gateways", data, None)

