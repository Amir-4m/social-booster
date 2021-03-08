import re
import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.cache import cache
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

    package = models.ForeignKey(Package, verbose_name=_('package'), on_delete=models.PROTECT)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f"order {self.id}"

    @property
    def owner_name(self):
        return f"{self.owner.phone_number}"


class AllowedGateway(models.Model):
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    updated_time = models.DateTimeField(_("updated time"), auto_now=True)
    version_pattern = models.CharField(_("pattern"), max_length=120)
    gateways_code = ArrayField(models.CharField(verbose_name=_('code'), max_length=10))

    class Meta:
        verbose_name = _("Allowed Gateway")
        verbose_name_plural = _('Allowed Gateways')

    @classmethod
    def get_gateways_by_version_name(cls, version_name):
        gateways = cache.get("gateways", [])
        allowed_gateways = []
        for gw in cls.objects.all():
            if re.match(gw.version_pattern, version_name):
                allowed_gateways = gw.gateways_code
                break

        for gateway in gateways:
            if gateway['code'] in allowed_gateways:
                yield gateway
