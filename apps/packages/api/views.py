from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.packages.api.serializers import PackageCategorySerializer, PackageSerializer
from apps.packages.models import PackageCategory
from utils.utils import get_members_count_based_on_link


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
        # filter the queryset to be dynamic, if its not the Not found error will be shown
        self.queryset = self.queryset.filter(is_dynamic_price=True)
        category_objects = self.get_object()
        serializer_data = PackageCategorySerializer(category_objects).data

        price_intervals = category_objects.intervals.values('amount_interval', 'price_per_interval')

        for package in serializer_data['packages']:
            members_count = get_members_count_based_on_link(request.GET.get('link'))
            suitable_interval_price = list(filter(lambda x: x['amount_interval'].lower <= members_count <= x['amount_interval'].upper,
                                                  price_intervals))[0]['price_per_interval']
            package['price'] = suitable_interval_price * members_count
            if package['discount'] != 0:
                # the package final_price should be computed here if the discount is not 0
                package['final_price'] = int(package['price'] - (package['price'] * (package['discount']/100)))
            else:
                package['final_price'] = package['price']

        return Response({'test': serializer_data})


