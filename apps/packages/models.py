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
    title = models.CharField(verbose_name=_('title'), max_length=50)
    slug = models.SlugField(verbose_name=_('slug'), max_length=50, unique=True, allow_unicode=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name="children", verbose_name=_("Parent"))
    description = models.TextField(_('Description'), blank=True)
    sort_by = models.PositiveSmallIntegerField(_('Sort'), default=0)
    is_enable = models.BooleanField(_("Is enable"), default=True)
    icon = models.ImageField(verbose_name=_("Package Icon"), upload_to='categories_icon')
    created_time = models.DateField(auto_now_add=True, verbose_name=_("Created time"))

    objects = PackageCategoryManager

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
            #     cat_dict["articles"] = Package.approves.filter(categories=cat)[:3]

            cat_list.append(cat_dict)

        return cat_list

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی پکیج'
        verbose_name_plural = 'دسته بندی های پکیج ها'


class Package(models.Model):
    created_time = models.DateField(auto_now_add=True, verbose_name=_("Created time"))
    updated_time = models.DateField(auto_now=True, verbose_name=_("Updated time"))

    name = models.CharField(_("Package name"), max_length=100, unique=True)
    category = models.ForeignKey(PackageCategory, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(verbose_name=_("Package price"))
    target_no = models.PositiveIntegerField(verbose_name=_("Request number"))
    discount = models.PositiveSmallIntegerField(_("discount"), default=0, help_text='در صورتی که صفر باشد در نظر گرفته نخواهد شد')
    is_enable = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {self.category.title}"

    def clean(self):
        if self.discount > 100:
            raise ValidationError('مقدار تخفیف بیش از ۱۰۰ درصد نمیتواند باشد')

    @staticmethod
    def get_enable_queryset():
        return Package.objects.filter(is_enable=True)

    class Meta:
        verbose_name = 'بسته'
        verbose_name_plural = 'بسته ها'






