from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.utils.translation import ugettext_lazy as _
from apps.packages.api.serializers import PackageCategorySerializer, PackageSerializer
from apps.packages.models import PackageCategory
from utils.utils import telegram_member_count


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
        # filter the queryset to be dynamic, if its not the Not found error will be shown
        self.queryset = self.queryset.filter(is_dynamic_price=True)
        category_objects = self.get_object()
        serializer_data = PackageCategorySerializer(category_objects).data

        price_intervals = category_objects.intervals.values('amount_interval', 'price_per_interval')

        for package in serializer_data['packages']:
            members_count = telegram_member_count(request.GET.get('link'))
            valid_interval_list = list(filter(lambda x: x['amount_interval'].lower <= members_count <= x['amount_interval'].upper,
                                              price_intervals))
            if len(valid_interval_list) > 0:
                suitable_interval_price = valid_interval_list[0]['price_per_interval']
                package['price'] = suitable_interval_price * members_count
                if package['discount'] != 0:
                    # the package final_price should be computed here if the discount is not 0
                    package['final_price'] = int(package['price'] - (package['price'] * (package['discount']/100)))
                else:
                    package['final_price'] = package['price']
            else:
                raise ValidationError(_("There is no interval for the given value"))

        return Response({'test': serializer_data})


