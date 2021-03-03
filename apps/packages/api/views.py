from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from apps.packages.api.serializers import PackageSerializer, PackageCategorySerializer
from apps.packages.models import Package, PackageCategory


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticated, ]


class PackageCategoryViewSet(ListModelMixin,
                      RetrieveModelMixin,
                      GenericViewSet):
    """

        list:
            Return all categories, ordered by most recently added.

            query parameters
            -  Ordering fields: 'id', 'title'. Ex: ?ordering=id
            -  Search fields: 'title' . Ex: ?search=some random name.
        retrieve:
            Return a specific category detail based on it's id.

    """
    serializer_class = PackageCategorySerializer
    queryset = PackageCategory.parents.filter(is_enable=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', ]
    ordering_fields = ['id', 'title']

    def get_queryset(self):
        if self.action == 'retrieve':
            return PackageCategory.objects.filter(is_enable=True)
        return super().get_queryset()


