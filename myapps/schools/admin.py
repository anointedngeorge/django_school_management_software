from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls.resolvers import URLPattern
from django_tenants.admin import TenantAdminMixin
from django.urls import path
from schools.models import Schools, LIST_SCHOOLS, Domain
from django.contrib import messages as djmessage
# Register your models here.
from schools.forms.index import SchoolForm

@admin.register(Schools)
class schoolsAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = LIST_SCHOOLS
    form = SchoolForm
    # list_filter = ['schema_name']

    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
    

    def get_urls(self):
        main_url = super().get_urls()
        custom_url = [
            path('deactivate-tenant/<int:tenant_id>/<str:tenant_name>/', self.deactivate_tenant, name='deactivatetenant'),
            path('activate-tenant/<int:tenant_id>/<str:tenant_name>/', self.activate_tenant, name='activatetenant'),
        ]
        return custom_url + main_url


    def deactivate_tenant(self, request,  **kwargs):
        applabel = self.opts.app_label
        modelname = self.model.__name__
        self.model.objects.filter(id=kwargs.get('tenant_id')).update(is_active=False)
        djmessage.warning(request, f"Users belonging to ({str(kwargs.get('tenant_name')).upper()}), will not be able to access their data. ")
        return redirect(f'/admin/{str(applabel).lower()}/{str(modelname).lower()}')


    def activate_tenant(self, request,  **kwargs):
        applabel = self.opts.app_label
        modelname = self.model.__name__
        self.model.objects.filter(id=kwargs.get('tenant_id')).update(is_active=True)
        djmessage.success(request, f"({str(kwargs.get('tenant_name')).upper()}) is active now. ")
        return redirect(f'/admin/{str(applabel).lower()}/{str(modelname).lower()}')

@admin.register(Domain)
class schoolsDomainAdmin(admin.ModelAdmin):
    list_display = ['domain','tenant','is_primary']