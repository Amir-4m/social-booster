from rest_framework import serializers

from apps.packages.models import Package, PackageCategory


class PackageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageCategory
        fields = '__all__'


class PackageSerializer(serializers.ModelSerializer):
    category = PackageCategorySerializer()

    class Meta:
        model = Package
        fields = ['id', 'name', 'category', 'price', 'discount', ]

