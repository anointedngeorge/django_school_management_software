
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.views.static import serve
from django.urls import path, include, re_path
from decouple import config
import importlib
from .admin import loadModuleAttribute


VERSION = 'v1'

SITE_ADMIN1 = loadModuleAttribute(f"{config('APP_MAIN_NAME')}.admin.base",'SITE_ADMIN1')
# prod_api = loadModuleAttribute(f"{config('APP_MAIN_NAME')}.api",'api')

urlpatterns = []


try:
    urlpatterns += [
        path(f"", SITE_ADMIN1.urls),
        # path(f"api/{VERSION}/", prod_api.urls, name='api'),
    ]
except Exception as e:
    urlpatterns += []