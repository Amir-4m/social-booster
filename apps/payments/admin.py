from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from apps.payments.models import Order, AllowedGateway


# Register your models here.
from apps.payments.services import CustomService


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    radio_fields = {'status': admin.HORIZONTAL}
    list_display = (
        'price', 'invoice_number', 'status',
        'gateway', 'is_paid', 'updated_time', 'created_time'
    )
    list_filter = ('is_paid', 'gateway', 'status')
    search_fields = ('owner__username', )


@admin.register(AllowedGateway)
class AllowedGatewayAdmin(admin.ModelAdmin):
    list_display = ('version_pattern', 'gateways_code')
    search_fields = ('version_name', 'gateways_code')



