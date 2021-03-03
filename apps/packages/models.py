from django.db import models


# Create your models here.
from rest_framework.exceptions import ValidationError


class PackageCategory(models.Model):
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, default=None, blank=True,
                               verbose_name='دسته بندی والد')
    title = models.CharField(max_length=100, unique=True, verbose_name='نام دسته بندی')
    icon = models.ImageField(verbose_name='آیکون دسته بندی')

    @property
    def children(self):
        return self.children

    @property
    def parents(self):
        all_parents = []
        current_parent = self.parent
        while current_parent:
            all_parents.append(current_parent)
            current_parent = current_parent.parent
        return all_parents

    @property
    def siblings(self):
        return PackageCategory.objects.filter(parent=self.parent).exclude(id=self.id)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی پکیج'
        verbose_name_plural = 'دسته بندی های پکیج ها'


class Package(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='نام بسته')
    category = models.ForeignKey(PackageCategory, on_delete=models.CASCADE, verbose_name='دسته بندی')
    price = models.PositiveIntegerField(verbose_name='هزینه بسته')
    target_no = models.PositiveIntegerField(verbose_name='تعداد درخواست')
    created = models.DateField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = models.DateField(auto_now=True, verbose_name='تاریخ به روزرسانی')
    discount = models.PositiveSmallIntegerField(default=0, verbose_name='تخفیف', help_text='در صورتی که صفر باشد در نظر گرفته نخواهد شد')
    is_enable_choices = (
        (True, 'هست'),
        (False, 'نیست')
    )
    is_enable = models.BooleanField(default=True, choices=is_enable_choices)

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






