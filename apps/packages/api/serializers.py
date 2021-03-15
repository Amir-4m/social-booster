from rest_framework import serializers

from apps.packages.models import Package, PackageCategory, PackageCategoryIntervalPrice


class PackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package
        fields = ('id', 'name', 'price')


class PackageCategoryIntervalPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PackageCategoryIntervalPrice
        fields = ('id', 'amount_interval', 'price_per_interval')


class PackageCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    packages = serializers.SerializerMethodField()
    package_intervals = serializers.SerializerMethodField()

    class Meta:
        model = PackageCategory
        fields = ('id', 'title', 'slug', 'children', 'packages', 'package_intervals', )

    def get_children(self, obj):
        return PackageCategorySerializer(obj.children.filter(is_enable=True), many=True).data
    
    def get_packages(self, obj):
        return PackageSerializer(Package.objects.filter(category=obj, is_enable=True), many=True).data

    def get_package_intervals(self, obj):
        return PackageCategoryIntervalPriceSerializer(PackageCategoryIntervalPrice.objects.filter(category=obj), many=True).data
