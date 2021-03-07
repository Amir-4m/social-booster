import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from apps.packages.models import Package


class Order(models.Model):
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    updated_time = models.DateTimeField(_("updated time"), auto_now=True)

    gateway = models.CharField(_('gateway'), max_length=50, blank=True, db_index=True)
    invoice_number = models.UUIDField(_('uuid'), unique=True, default=uuid.uuid4, editable=False)
    transaction_id = models.CharField(_('transaction id'), unique=True, null=True, max_length=40)
    is_paid = models.BooleanField(_("is paid"), null=True)
    price = models.PositiveIntegerField(_('price'))
    version_name = models.CharField(_('version name'), max_length=50)
    redirect_url = models.CharField(_('redirect url'), max_length=120)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f"order {self.id}"

    @property
    def owner_name(self):
        return f"{self.owner.phone_number}"
