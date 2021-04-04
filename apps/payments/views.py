from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from apps.payments.models import Order
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
        return redirect(reverse('admin:payments_allowedgateway_changelist'))


class PaymentView(View):
    def get(self, request, *args, **kwargs):
        transaction_id = request.GET.get('transaction_id')
        purchase_verified = request.GET.get('purchase_verified')
        if purchase_verified is None:
            return HttpResponse('وضعیت سفارش نا معتبر می باشد !')

        purchase_verified = purchase_verified.lower().strip()

        try:
            order = Order.objects.select_related('package').get(
                transaction_id=transaction_id,
                is_paid=None
            )
        except Order.DoesNotExist:
            return HttpResponse('سفارشی یافت نشد !')

        except Order.MultipleObjectsReturned:
            return HttpResponse('')

        if purchase_verified == 'true':
            html = 'payments/payment_done.html'
            order.is_paid = True

        else:
            html = 'payments/payment_failed.html'
            order.is_paid = False

        order.save()
        context = {
            "redirect_url": order.redirect_url,
            "purchase_verified": purchase_verified
        }
        return render(request, html, context)
