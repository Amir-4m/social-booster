from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import setttings

from apps.packages.models import Package


class Order(models.Model):
    STATUS_ENABLE = 0
    STATUS_COMPLETE = 1
    STATUS_DISABLE = 2

    STATUS_CHOICES = [
        (STATUS_ENABLE, _('enabled')),
        (STATUS_COMPLETE, _('completed')),
        (STATUS_DISABLE, _('disabled')),
    ]
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=STATUS_ENABLE)
    package = models.ForeignKey(Package, on_delete=models.PROTECT, verbose_name=_("Package name"))
    link = models.TextField(_("link"))
    description = models.TextField(verbose_name=_("Description"))
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('Owner'))
    created_time = models.DateField(auto_now_add=True, verbose_name=_("Create time"))
    updated_time = models.DateField(auto_now=True, verbose_name=_("Update time"))

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

    def __str__(self):
        return self.package.name

    @property
    def owner_name(self):
        return f"{self.owner.phone_number} {self.owner.first_name} {self.owner.last_name}"
