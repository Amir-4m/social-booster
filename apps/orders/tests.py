import random
from unittest import mock
from unittest.mock import patch

import requests
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase

from apps.orders.models import AllowedGateway
from apps.packages.models import Package, PackageCategory
from utils.test_utils import rand_string


class TestOrderGateway(APITestCase):
    def setUp(self):
        icon = \
            requests.get("https://www.flaticon.com/svg/vstatic/svg/174/174855.svg?token=exp=1615116565~hmac=40ba779160f307e314c0b97fc53d9c59").content
        icon_file = SimpleUploadedFile('gravatar.jpg', icon, 'image/jpeg')

        number_of_parents = 10
        for i in range(number_of_parents):
            parent_package = PackageCategory.objects.create(
                title=f"Parent {i}-{rand_string()}",
                slug=f"parent-{i}-{rand_string()}",
                parent=None,
                description=f"Description Package {i}",
                sort_by=i,
                is_enable=i % 2,
                icon=icon_file
            )
            for c in range(random.randint(11, 30)):
                PackageCategory.objects.create(
                    title=f"Parent {c} - {rand_string()}",
                    slug=f"parent-{c}-{rand_string()}",
                    parent=parent_package,
                    description=f"Description Package {c}",
                    sort_by=i,
                    is_enable=i % 2,
                    icon=icon_file
                )
        self.package = Package.objects.create(
            name="Golden",
            category=random.choice(PackageCategory.objects.parents()),
            price=10000,
            target_no=200,
            is_enable=True
        )
        self.gateway = AllowedGateway(
            gateways_code='SAMAN'
        )



