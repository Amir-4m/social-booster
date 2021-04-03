from django.contrib import admin
import apps.packages.models as package_models


# Register your models here.
@admin.register(package_models.Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount', 'final_price', 'created_time',
                    'updated_time', 'is_enable', ]
    search_fields = ['name', ]
    list_filter = ['category', ]


class PackageCategoryIntervalPriceInline(admin.TabularInline):
    model = package_models.PackageCategoryIntervalPrice


class PackageCategoryDynamicValueInline(admin.TabularInline):
    model = package_models.PackageCategoryDynamicValue


@admin.register(package_models.PackageCategory)
class PackageCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "id",  "slug", "sort_by", "parent", "created_time", "is_enable")
    search_fields = ('title', 'slug')
    prepopulated_fields = {"slug": ("title",)}
    list_select_related = ('parent', )
    autocomplete_fields = ('parent', )
    inlines = [PackageCategoryIntervalPriceInline, PackageCategoryDynamicValueInline, ]


@admin.register(package_models.PackageCategoryIntervalPrice)
class PackageCategoryIntervalPriceAdmin(admin.ModelAdmin):
    list_filter = ['category', ]
    search_fields = ['category__name', ]


@admin.register(package_models.PackageCategoryDynamicValue)
class PackageCategoryDynamicValueAdmin(admin.ModelAdmin):
    list_display = ['title', 'value_type', 'required']
    list_filter = ['category', ]
    search_fields = ['category__name', ]


