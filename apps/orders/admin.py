from django.contrib import admin
import apps.orders.models as orders_model


# Register your models here.
@admin.register(orders_model.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['owner_name', 'status', 'description',
                    'created_time', 'updated_time']
    search_fields = ['package__name',
                     'owner__name', ]
    list_filter = ['status', ]

