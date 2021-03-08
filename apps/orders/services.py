import requests
from django.conf import settings


class CustomService(object):

    @staticmethod
    def payment_request(endpoint, method, data=None):
        headers = {
            "Authorization": f"TOKEN {settings.PAYMENT_SERVICE_SECRET}",
            "Content-Type": "application/json"
        }
        methods = {
            'get': requests.get,
            'post': requests.post
        }

        _r = methods[method](f"{settings.PAYMENT_API_URL}{endpoint}/", headers=headers, json=data, timeout=(3.05, 9))
        _r.raise_for_status()
        return _r.json()
