from rest_framework.throttling import ScopedRateThrottle


class PhoneNumberScopedRateThrottle(ScopedRateThrottle):

    def get_cache_key(self, request, view):
        if 'phone_number' in request.data:
            ident = request.data['phone_number']
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident,
        }
