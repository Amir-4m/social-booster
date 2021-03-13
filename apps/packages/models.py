from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from rest_framework.exceptions import ValidationError


class PackageCategoryManager(models.Manager):

    def live(self):
        qs = self.get_queryset()
        return qs.filter(is_enable=True)

    def parents(self):
        qs = self.live()
        return qs.filter(parent__isnull=True)


class PackageCategory(models.Model):
    created_time = models.DateField(_("created time"), auto_now_add=True)
    updated_time = models.DateField(_("updated time"), auto_now=True)

    title = models.CharField(_('title'), max_length=50)
    slug = models.SlugField(_('slug'), max_length=50, unique=True, allow_unicode=True)
    parent = models.ForeignKey('self', verbose_name=_("parent"), blank=True, null=True, on_delete=models.CASCADE, related_name="children")
    description = models.TextField(_('description'), blank=True)
    sort_by = models.PositiveSmallIntegerField(_('sort'), default=0)
    is_enable = models.BooleanField(_("is enable"), default=True)
    icon = models.ImageField(_("package Icon"), upload_to='categories_icon')

    objects = PackageCategoryManager()

    class Meta:
        ordering = ['sort_by', 'id', ]
        verbose_name = 'Package category'
        verbose_name_plural = 'Package categories'

    def __str__(self):
        return self.title

    @classmethod
    def category_tree(cls, cat_parent=None):
        qs = cls.objects.filter(is_enable=True)
        if cat_parent is None:
            qs = qs.filter(parent__isnull=True)
        else:
            qs = qs.filter(parent=cat_parent)

        cat_list = []
        for cat in qs:
            cat_dict = {
                "category": cat,
                "subs": cls.category_tree(cat)
            }

            # if not cat_dict["subs"]:
            #     cat_dict["packages"] = Package.objects.live().filter(categories=cat)

            cat_list.append(cat_dict)

        return cat_list


class PackageManager(models.Manager):

    def live(self):
        qs = self.get_queryset()
        return qs.filter(is_enable=True)


class Package(models.Model):
    created_time = models.DateField(_("created time"), auto_now_add=True)
    updated_time = models.DateField(_("updated time"), auto_now=True)

    name = models.CharField(_("package name"), max_length=100)
    category = models.ForeignKey(PackageCategory, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(_('price'))
    price_offer = models.PositiveIntegerField(_('price offer'), null=True, blank=True)
    amount = models.PositiveIntegerField(_('amount'))
    description = models.TextField(_('description'), default="")
    sku = models.CharField(_('package sku'), max_length=40, unique=True, null=True)
    featured = models.DateTimeField(null=True, blank=True,
                                    help_text=_('if this date field is specified, the coin package will be featured until this date'))
    is_enable = models.BooleanField(default=True)

    objects = PackageManager()

    @property
    def price_value(self):
        return self.price_offer or self.price

    @property
    def sku_value(self):
        return self.sku if self.sku else None

    def __str__(self):
        return f"{self.name} {self.category.title}"








