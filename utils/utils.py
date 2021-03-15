import logging
import requests

from collections import defaultdict

from django.core.cache import caches
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from khayyam import JalaliDatetime


logger = logging.getLogger('accounts')


class ApprovedListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('approved')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'approved'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('approved', _('approved')),
            ('not-approved', _('not approved')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # to decide how to filter the queryset.
        if self.value() == 'approved':
            queryset = queryset.exclude(approved_user__isnull=True)
            return queryset
        if self.value() == 'not-approved':
            queryset = queryset.filter(approved_user__isnull=True)
            return queryset


class ApprovedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(approved_time__isnull=False, approved_user__isnull=False, is_enable=True)


# def article_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT /articles/<article's title-filename>
#     return f"articles/{filename}"


def filter_category_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT /filters/categories/<category's title-filename>
    return f"filters/categories/{timezone.now().microsecond}-{filename}"


def profile_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT /profiles/<profile's title-filename>
    return f"profiles/{instance.user.first_name}-{filename}"

maketrans = lambda A, B: dict((ord(a), b) for a, b in zip(A, B))
number_converter = maketrans(
    u'١٢٣٤٥٦٧٨٩٠۱۲۳۴۵۶۷۸۹۰٤٥٦₀₁₂₃₄₅₆₇₈₉¹²⁰⁴⁵⁶⁷⁸⁹①②③④⑤⑥⑦⑧⑨⑴⑵⑶⑷⑸⑹⑺⑻⑼⒈⒉⒊⒋⒌⒍⒎⒏⒐',
    u'123456789012345678904560123456789120456789123456789123456789123456789'
)


def send_msg(phone_number, message):
    data = {
        "data": [
            {
                "text": message,
                "phone_numbers": [phone_number]
            }
        ]
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Token {settings.SMS_GATE_WAY_TOKEN}"
    }
    r = object

    try:
        r = requests.post(
            headers=headers,
            url=settings.SMS_GATE_WAY_URL,
            json=data,
            timeout=(3, 6)
        )
        r.raise_for_status()
    except requests.HTTPError as e:
        logger.error(
            f"[HTTP exception occurred while sending SMS]"
            f"-[func-name: {send_msg.__name__}]"
            f"-[response: {r.content}]"
            f"-[phone-number: {phone_number}]"
            f"-[error: {e}]"
            f"-[message: {message}]"
        )
        return False
    except Exception as e:
        logger.error(
            f"[Bare exception occurred while sending SMS]"
            f"-[func-name: {send_msg.__name__}]"
            f"-[phone-number: {phone_number}]"
            f"-[error: {e}]"
            f"-[message: {message}]"
        )
        return False
    logger.info(
        f"[SMS sent successfully]"
        f"-[func-name: {send_msg.__name__}]"
        f"-[response: {r.content}]"
        f"-[phone-number: {phone_number}]]"
        f"-[message: {message}]"
    )
    return True


class JalaliTimeMixin:
    @property
    def jalali_published_time(self):
        if self.approved_time:
            return JalaliDatetime(self.approved_time).strftime('%C')
        return ''

