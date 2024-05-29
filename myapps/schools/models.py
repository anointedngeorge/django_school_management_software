from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.urls import reverse, reverse_lazy
from django.utils.html import format_html

LIST_SCHOOLS = ['schema_name','school_name','school_phone','school_address','_domain','_status','_action']
class Schools(TenantMixin):
    
    school_name = models.CharField(max_length=100)
    school_phone = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True, choices=[(True,'Active'), (False,"Suspended")])
    school_address = models.TextField()
    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return self.schema_name
    
    class Meta:
        verbose_name = 'school'
        verbose_name_plural = 'Schools'

    def _domain(self):
        return self.get_primary_domain()
    
    def _status(self):
        message = ""
        if self.is_active:
            message = "<span class='text text-success'>Active</span>"
        else:
            message = "<span class='text text-danger'>Suspended</span>"
        return format_html(f"<small>{message}</small>")
    
    def _action(self):
        try:
            if self.is_active: 
                url = reverse("admin:deactivatetenant", kwargs={'tenant_id':self.pk,'tenant_name':self.schema_name})
                return format_html(f"<a href='{url}' class='btn btn-sm btn-danger'>OFF</a>" )
            else:
                url = reverse("admin:activatetenant", kwargs={'tenant_id':self.pk,'tenant_name':self.schema_name})
                return format_html(f"<a href='{url}' class='btn btn-sm btn-success'>ON</a>")
            
        except:
            pass

    def _deactivate(self):
        tenant_id = 2
        try:
            m = self._meta.model
            tenant = m.objects.get(pk=tenant_id)
            tenant.is_active = False  # Set is_active to False
            tenant.save()
            print(f"Tenant {tenant_id} deactivated successfully.")
        except m.DoesNotExist:
            print(f"Tenant {tenant_id} does not exist.")
    

class Domain(DomainMixin):
    pass