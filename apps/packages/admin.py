from django.contrib import admin
import apps.packages.models as package_models


# Register your models here.
@admin.register(package_models.Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount', 'created_time',
                    'updated_time', 'is_enable', ]
    search_fields = ['name', ]
    list_filter = ['category', ]


@admin.register(package_models.PackageCategory)
class PackageCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "sort_by", "parent", "created_time", "is_enable")
    search_fields = ('title', 'slug')
    prepopulated_fields = {"slug": ("title",)}
    list_select_related = ('parent', )
    autocomplete_fields = ('parent', )




