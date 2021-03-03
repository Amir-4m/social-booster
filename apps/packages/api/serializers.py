from rest_framework import serializers

from apps.packages.models import Package, PackageCategory


class PackageCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = PackageCategory
        fields = ('id', 'title', 'slug', 'children')

    def get_children(self, obj):
        return PackageCategorySerializer(obj.children.filter(is_enable=True), many=True).data


class PackageSerializer(serializers.ModelSerializer):
    category = PackageCategorySerializer()

    class Meta:
        model = Package
        fields = ['id', 'name', 'category', 'price', 'discount', ]

