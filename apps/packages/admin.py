from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.forms import ModelForm
from apps.packages.models import Package, PackageCategory, PackageCategoryIntervalPrice, PackageCategoryForm


class PackageAdminForm(ModelForm):

    class Meta:
        model = Package
        exclude = ['updated_time', 'created_time']

    def clean_featured(self):
        banner = self.files.get('banner_image')
        featured = self.cleaned_data['featured']

        if featured and not self.instance.banner_image and not banner:
            raise ValidationError(_('featured package should have a banner image.'))
        return featured


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    form = PackageAdminForm
    list_display = ['name', 'price', 'discount', 'final_price', 'category', 'updated_time', 'is_enable']
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


