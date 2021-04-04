import logging

from django.db import transaction
from django.urls import reverse
from rest_framework import viewsets, views
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.payments.api.serializers import OrderSerializer, OrderGatewaySerializer, PurchaseSerializer
from apps.payments.models import Order, AllowedGateway
from apps.payments.services import CustomService

logger = logging.getLogger(__name__)


class OrderViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication, )
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OrderGateWayAPIView(views.APIView):
    authentication_classes = (JWTAuthentication,)
    """Set an gateway for a package order to get the payment url"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = OrderGatewaySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        package_order = serializer.validated_data['package_order']
        gateway = serializer.validated_data['gateway']
        try:
            _r = CustomService.payment_request(
                'orders',
                'post',
                data={
                    'gateway': gateway,
                    'price': package_order.package.price_value,
                    'service_reference': str(package_order.invoice_number),
                    'is_paid': package_order.is_paid,
                    "redirect_url": request.build_absolute_uri(reverse('payment-done')),
                    "sku": package_order.package.sku,
                    "package_name": settings.CAFE_BAZAAR_PACKAGE_NAME
                }
            )
            transaction_id = _r.get('transaction_id')
            try:
                for gw in list(AllowedGateway.get_gateways_by_version_name(package_order.version_name)):
                    if gw['id'] == gateway:
                        package_order.gateway = gw['display_name']
            except Exception as e:
                logger.warning(f'could not fetch gateway for order {package_order.id}: {e}')
                pass
            package_order.transaction_id = transaction_id
            package_order.description = serializer.validated_data['description']
            package_order.extras = serializer.validated_data['extras']
            package_order.save()
        except Exception as e:
            logger.error(f"error calling payment with endpoint orders and action post: {e}")
            raise ValidationError(detail={'detail': _('error in submitting order gateway')})

        try:
            response = CustomService.payment_request(
                'purchase/gateway',
                'post',
                data={'order': str(package_order.invoice_number), 'gateway': gateway}
            )
        except Exception as e:
            logger.error(f"error calling payment with endpoint purchase/gateway and action post: {e}")
            raise ValidationError(detail={'detail': _('error in getting order gateway')})

        return Response(data=response)


class PurchaseVerificationAPIView(views.APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        purchase_verified = False
        serializer = PurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        gateway_code = serializer.validated_data['gateway_code']
        purchase_token = serializer.validated_data.get('purchase_token')
        package_order = serializer.validated_data['package_order']
        with transaction.atomic():
            order = Order.objects.select_related('package').get(id=package_order.id)
            if gateway_code == "BAZAAR":
                try:
                    _r = CustomService.payment_request(
                        'purchase/verify',
                        'post',
                        data={
                            'order': str(order.invoice_number),
                            'purchase_token': purchase_token
                        }
                    )
                    purchase_verified = _r['purchase_verified']
                except Exception as e:
                    logger.error(f"error calling payment with endpoint purchase/verify and action post: {e}")
                    raise ValidationError(detail={'detail': _('error in verifying purchase')})

            # the order is_paid is set here
            order.is_paid = purchase_verified
            order.save()

        return Response({'purchase_verified': purchase_verified})


