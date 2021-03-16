from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.packages.api.serializers import PackageCategorySerializer
from apps.packages.models import PackageCategory


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

    @action(methods=['get'], detail=True)
    def compute(self, request, *args, **kwargs):
        # TODO : here the price of packages should be computed and it also needs a link in the query params
        return Response({'test': PackageCategorySerializer(self.get_object()).data})


