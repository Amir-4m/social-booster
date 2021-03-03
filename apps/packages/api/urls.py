from django.urls import path
from rest_framework import routers

from apps.packages.api.views import PackageCategoryViewSet, PackageViewSet

router = routers.SimpleRouter()
router.register(r'categories', PackageCategoryViewSet, basename='categories')
router.register(r'packages', PackageViewSet, basename='packages')

urlpatterns = router.urls
