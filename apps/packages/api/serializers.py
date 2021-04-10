from rest_framework import serializers

from apps.packages.models import Package, PackageCategory, PackageCategoryForm


class PackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Package
        fields = ('id', 'name', 'amount', 'sku', 'price', 'discount', 'final_price', )


class PackageCategoryFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = PackageCategoryForm
        fields = ('title', 'key', 'description', 'value_type', 'required', )


class PackageCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    packages = serializers.SerializerMethodField()
    form_fields = serializers.SerializerMethodField()

    class Meta:
        model = PackageCategory
        fields = ('id', 'title', 'icon', 'slug', 'is_dynamic_price', 'children', 'form_fields', 'packages', 'input_label', )

    def get_children(self, obj):
        return PackageCategorySerializer(obj.children.filter(is_enable=True), many=True, context=self.context).data
    
    def get_packages(self, obj):
        return PackageSerializer(Package.objects.filter(category=obj, is_enable=True), many=True).data

    def get_form_fields(self, obj):
        return PackageCategoryFormSerializer(PackageCategoryForm.objects.filter(category=obj), many=True).data


