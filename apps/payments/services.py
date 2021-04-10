import logging
import requests

from django.conf import settings

logger = logging.getLogger(__name__)


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

        try:
            _r = methods[method](f"{settings.PAYMENT_API_URL}{endpoint}/", headers=headers, json=data, timeout=(3.05, 30))
            _r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.warning(f'[payment gateway]-[HTTPError]-[endpoint: {endpoint}]-[status code: {e.response.status_code}]-[err: {e.response.text}]')
            raise
        except requests.exceptions.ConnectTimeout as e:
            logger.critical(f'[payment gateway]-[ConnectTimeout]-[endpoint: {endpoint}]-[err: {e}]')
            raise
        except Exception as e:
            logger.error(f'[payment gateway]-[{type(e)}]-[endpoint: {endpoint}]-[err: {e}]')
            raise

        return _r.json()
