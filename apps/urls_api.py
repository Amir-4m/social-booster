from django.conf.urls import url
from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path('accounts/', include("apps.accounts.api.urls")),
    path('payments/', include("apps.payments.api.urls")),
    path('packages/', include("apps.packages.api.urls")),
    url(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('v1/docs/', schema_view),
]
