"""socialboost URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework.documentation import include_docs_urls

from django.conf import settings


urlpatterns = [
    path('admin52f930/', admin.site.urls),
    # API views
    path('api/v1/', include("apps.urls_api")),
    path('orders/', include("apps.payments.urls")),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('tinymce/', include('tinymce.urls')),

    path('docs/', include_docs_urls(title='Social Booster')),
]

if settings.DEVEL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
