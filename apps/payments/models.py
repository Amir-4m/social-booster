import logging
import re
import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.cache import cache
from apps.packages.models import Package

logger = logging.getLogger(__name__)


class Order(models.Model):
    WAITING_FOR_APPROVE = 'w8_for_approve'
    PENDING_STATUS = 'pending'
    REJECT_STATUS = 'reject'
    INACTIVE_STATUS = 'inactive'
    RUNNING_STATUS = 'running'
    DONE_STATUS = 'done'

    ORDER_STATUS_CHOICES = (
        (WAITING_FOR_APPROVE, _('waiting for approve')),
        (PENDING_STATUS, _('pending')),
        (REJECT_STATUS, _('reject')),
        (INACTIVE_STATUS, _('inactive')),
        (RUNNING_STATUS, _('running')),
        (DONE_STATUS, _('done')),
    )
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    updated_time = models.DateTimeField(_("updated time"), auto_now=True)

    gateway = models.CharField(_('gateway'), max_length=50, blank=True, db_index=True)
    invoice_number = models.UUIDField(_('uuid'), unique=True, default=uuid.uuid4, editable=False)
    transaction_id = models.CharField(_('transaction id'), unique=True, null=True, max_length=40)
    is_paid = models.BooleanField(_("is paid"), null=True, editable=False)
    status = models.CharField(_("status"), max_length=14, choices=ORDER_STATUS_CHOICES, default=WAITING_FOR_APPROVE)

    extras = models.JSONField(_("extra data"), default=dict)
    description = models.TextField(_("description"), blank=True)
    price = models.PositiveIntegerField(_('price'))
    amount = models.PositiveIntegerField(_('amount'), default=0)
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
        gateways_list = []

        try:
            for gw in cls.objects.all():
                if re.match(gw.version_pattern, version_name):
                    allowed_gateways = gw.gateways_code
                    break
            for gateway in gateways:
                if gateway['code'] in allowed_gateways:
                    gateways_list.append(gateway)
        except Exception as e:
            logger.error(f'getting gateways by version name {version_name} failed: {e}')

        return gateways_list

