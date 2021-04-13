import logging
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from apps.packages.api.serializers import PackageSerializer
from apps.payments.models import Order, AllowedGateway

logger = logging.getLogger(__name__)


class OrderSerializer(serializers.ModelSerializer):
    gateways = serializers.SerializerMethodField(read_only=True)
    package_detail = PackageSerializer(read_only=True)

    class Meta:
        model = Order
        exclude = ('owner', )
        extra_kwargs = {'extras': {'write_only': True}}

    def get_gateways(self, obj):
        gateways_list = []
        if self.context['view'].action != 'create':
            return gateways_list

        gateways_list = AllowedGateway.get_gateways_by_version_name(obj.version_name)
        return gateways_list


class OrderGatewaySerializer(serializers.Serializer):
    gateway = serializers.IntegerField()
    package_order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.filter(is_paid=None))

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class PurchaseSerializer(serializers.Serializer):
    purchase_token = serializers.CharField(max_length=50, allow_null=True)
    gateway_code = serializers.CharField(max_length=10)
    package_order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.filter(is_paid=None))

    def validate(self, attrs):
        gateway_code = attrs['gateway_code']
        purchase_token = attrs.get('purchase_token')
        if gateway_code == 'BAZAAR' and purchase_token is None:
            raise ValidationError(detail={'detail': _('purchase_token is required for gateway bazaar!')})
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


