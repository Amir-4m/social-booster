from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from apps.payments.models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {'extras': {'write_only': True}}


class OrderGatewaySerializer(serializers.Serializer):
    gateway = serializers.IntegerField()
    description = serializers.CharField()
    extras = serializers.JSONField(required=False)
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


