from django.contrib.postgres.fields import IntegerRangeField
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _


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
    input_label = models.CharField(_('input label'), blank=True, max_length=100,
                                   help_text=_("The label that is shown next to input user"))
    is_dynamic_price = models.BooleanField(_("is dynamic price"), default=False,
                                           help_text=_("Indicate that the category price should dynamically be calculated on the client side or not"))
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


class PackageCategoryIntervalPrice(models.Model):
    created_time = models.DateField(_("created time"), auto_now_add=True)
    updated_time = models.DateField(_("updated time"), auto_now=True)

    category = models.ForeignKey(PackageCategory, verbose_name=_("category"), on_delete=models.CASCADE, related_name='intervals')
    amount_interval = IntegerRangeField(_('the amount interval'),
                                        help_text=_("the left input indicate the lower bound of interval and the right one show upper bound"))
    price_per_interval = models.PositiveIntegerField(_('price'), help_text=_("price for each interval, for example from 100 to 1000 has a price"))

    def __str__(self):
        return f"{self.category.title} {self.amount_interval} -- {self.price_per_interval}"


class PackageManager(models.Manager):

    def live(self):
        qs = self.get_queryset()
        return qs.filter(is_enable=True)


class Package(models.Model):
    created_time = models.DateField(_("created time"), auto_now_add=True)
    updated_time = models.DateField(_("updated time"), auto_now=True)

    name = models.CharField(_("package name"), max_length=100)
    category = models.ForeignKey(PackageCategory, on_delete=models.CASCADE, related_name="packages")
    price = models.PositiveIntegerField(_('price'), null=True, blank=True)
    discount = models.PositiveSmallIntegerField(_("discount"), validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                help_text=_("The discount percent for package value should be in [1, 100]"), default=0)
    amount = models.PositiveIntegerField(_('amount'))
    description = models.TextField(_('description'), default="")
    sku = models.CharField(_('package sku'), max_length=40, unique=True, null=True)
    featured = models.DateTimeField(null=True, blank=True,
                                    help_text=_('if this date field is specified, the coin package will be featured until this date'))
    is_enable = models.BooleanField(default=True)

    objects = PackageManager()

    @property
    def final_price(self):
        if self.price is None:
            return None
        return int(self.price - (self.price * (self.discount/100)))

    def __str__(self):
        return f"{self.name} {self.category.title}"
