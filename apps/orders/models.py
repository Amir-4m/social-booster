from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from apps.packages.models import Package


class Order(models.Model):
    package = models.ForeignKey(Package, on_delete=models.PROTECT, verbose_name=_("Package name"))
    link = models.URLField(verbose_name=_("Link"))
    description = models.TextField(verbose_name=_("Description"))
    created_time = models.DateField(auto_now_add=True, verbose_name=_("Create time"))
    updated_time = models.DateField(auto_now=True, verbose_name=_("Update time"))

    def __str__(self):
        return self.package.name

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'


