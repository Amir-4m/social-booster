from django.urls import path, include

urlpatterns = [
    path('accounts/', include("apps.accounts.api.urls")),
    path('orders/', include("apps.orders.api.urls")),
    path('namads/', include("apps.packages.api.urls")),

    # path('v1/docs/', schema_view),
]
