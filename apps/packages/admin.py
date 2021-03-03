from django.contrib import admin
import apps.packages.models as package_models


# Register your models here.
@admin.register(package_models.Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name', ]


@admin.register(package_models.PackageCategory)
class PackageCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', ]



