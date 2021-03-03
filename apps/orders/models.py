from django.db import models


# Create your models here.
from apps.packages.models import Package


class Order(models.Model):
    package = models.ForeignKey(Package, on_delete=models.PROTECT, verbose_name='نام بسته')
    link = models.URLField(verbose_name='آدرس ویدیو')
    description = models.TextField(verbose_name='توضیحات تکمیلی')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.package.name

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'


