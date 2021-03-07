import random
import string

import requests
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.conf import settings
from apps.packages.models import PackageCategory


def rand_string():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))


class TestPackageCategories(APITestCase):
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

    def test_get_categories(self):
        url = reverse('categories-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)




