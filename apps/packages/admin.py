from django.contrib import admin
from apps.packages.models import Package, PackageCategory, PackageCategoryIntervalPrice, PackageCategoryForm


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount', 'final_price', 'category', 'updated_time', 'is_enable', ]
    search_fields = ['name', ]
    list_filter = ['category', ]


class PackageCategoryIntervalPriceInline(admin.TabularInline):
    model = PackageCategoryIntervalPrice
    extra = 1


class PackageCategoryFormInline(admin.TabularInline):
    model = PackageCategoryForm
    extra = 1


@admin.register(PackageCategory)
class PackageCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "id",  "slug", "sort_by", "parent", "created_time", "is_enable")
    search_fields = ('title', 'slug')
    prepopulated_fields = {"slug": ("title",)}
    list_select_related = ('parent', )
    autocomplete_fields = ('parent', )
    inlines = [PackageCategoryIntervalPriceInline, PackageCategoryFormInline, ]


