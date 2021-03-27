from abc import ABC

from rest_framework import serializers

from apps.packages.models import Package, PackageCategory


class PackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package
        fields = ('id', 'name', 'amount', 'price', 'discount', 'final_price', )


class PackageCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    packages = serializers.SerializerMethodField()

    class Meta:
        model = PackageCategory
        fields = ('id', 'title', 'icon', 'slug', 'is_dynamic_price', 'children', 'packages', 'input_label', )

    def get_children(self, obj):
        return PackageCategorySerializer(obj.children.filter(is_enable=True), many=True, context=self.context).data
    
    def get_packages(self, obj):
        return PackageSerializer(Package.objects.filter(category=obj, is_enable=True), many=True).data

