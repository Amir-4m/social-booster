from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from apps.payments.services import CustomService
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _


class SyncGatewayView(View):

    def get(self, request):
        # the gateways should be synced here
        if request.user.is_superuser:
            data = CustomService.payment_request('gateways', 'get')
            cache.set("gateways", data, None)
            gateways = cache.get("gateways", [])
            messages.success(request, _(f"{len(gateways)} gateways are added"))
        return redirect('/admin52f930/payments/allowedgateway/')

