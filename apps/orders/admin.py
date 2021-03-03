from django.contrib import admin
import apps.orders.models as orders_model


# Register your models here.
@admin.register(orders_model.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = []

