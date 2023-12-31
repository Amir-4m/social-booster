from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.utils.translation import ugettext_lazy as _
from apps.packages.api.serializers import PackageCategorySerializer, PackageSerializer, PackageSliderSerializer
from apps.packages.models import PackageCategory, Package, PackageCategoryIntervalPrice
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
    queryset = PackageCategory.objects.filter(is_enable=True)

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(parent__isnull=True)
        return super().get_queryset()

    @action(methods=['get'], detail=True)
    def compute(self, request, *args, **kwargs):
        # filter the queryset to be dynamic, if its not the Not found error will be shown
        package_category = self.get_object()
        if not package_category.is_dynamic_price:
            raise ValidationError(_("This category does not support dynamic prices"))
        packages = Package.objects.filter(category=package_category)
        # validate and prepare the link
        link = request.GET.get('link')

        # get members count for the given URL
        try:
            if 'http' in link:
                link = link.split('/')[-1]
            else:
                link = link.replace('@', '')

            members_count = telegram_member_count(link)
        except Exception as e:
            raise ValidationError(_(f"{link} is not a valid or accessible URL"))

        # Fetch the related interval
        try:
            valid_interval = package_category.intervals.get(amount_interval__contains=members_count)
        except PackageCategoryIntervalPrice.DoesNotExist:
            raise ValidationError(_(f"No matching interval for the given members count {members_count}"))

        # calculate dynamic prices
        for package in packages:
            package.price = valid_interval.price_per_interval * members_count

        # return the result
        return Response(PackageSerializer(packages, many=True).data)

    @action(methods=['get'], detail=False, serializer_class=PackageSliderSerializer)
    def sliders(self, request, *args, **kwargs):
        """Sliders
            category_id and banner_image of Packages that are featured
        """
        data = Package.objects.filter(
            featured__gte=timezone.now()
        )
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)


