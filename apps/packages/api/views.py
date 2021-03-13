from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from apps.packages.api.serializers import PackageSerializer, PackageCategorySerializer
from apps.packages.models import Package, PackageCategory


class PackageCategoryViewSet(ListModelMixin,
                             RetrieveModelMixin,
                             GenericViewSet):
    """
        list:
            Return all categories

            query parameters
            -  Ordering fields: 'id', 'title'. Ex: ?ordering=id
        retrieve:
            Return a specific category detail based on it's id.
    """
    serializer_class = PackageCategorySerializer
    queryset = PackageCategory.objects.filter(is_enable=True, parent__isnull=True)

    def get_queryset(self):
        if self.action == 'retrieve':
            return PackageCategory.objects.filter(is_enable=True)
        return super().get_queryset()


