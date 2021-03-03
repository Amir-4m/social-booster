from rest_framework import routers

from apps.orders.api.views import OrderViewSet

router = routers.SimpleRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = router.urls

