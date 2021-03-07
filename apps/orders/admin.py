from django.contrib import admin
import apps.orders.models as orders_model


# Register your models here.
@admin.register(orders_model.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'price', 'invoice_number',
        'gateway', 'is_paid', 'updated_time', 'created_time'
    )
    list_filter = ('is_paid', 'gateway', )
    search_fields = ('owner__username', )

