
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from api.versions.v1.route.dev_route import api

VERSION = 'v1'

handler404 = 'error_handlers.views.handler_404'

urlpatterns = [
    path('tenant/admin/', admin.site.urls),
    path('', include("admin_dashboard.urls")),
    # api
    path(f'api/{VERSION}/', api.urls),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]
