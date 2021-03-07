from django.urls import path
from rest_framework import routers

from apps.packages.api.views import PackageCategoryViewSet

router = routers.SimpleRouter()
router.register(r'categories', PackageCategoryViewSet, basename='categories')

urlpatterns = router.urls
