from django.db import models
from django.utils import timezone
from decouple import config
from ..user_permissions_context import UserPermissions
from django.contrib.sessions.models import Session
from ..plugins.custom_plugins import generate_filename
from ..core_attrs import CoreAttrs
from ..core import CoreBaseModel
from ..actions.custom_action1 import change_url
from django.conf import settings
from django import forms



class Plugins(models.Model):
    
    plugin_type =  models.CharField(max_length=150)
    status = models.BooleanField(default=False, choices=[
        (True, "Activate"),
        (False,"Deactivate")
    ])
    name = models.CharField(max_length=150)
    file_path = models.CharField(max_length=250, null=True, blank=True)
    template_file = models.CharField(max_length=250, null=True, blank=True)
    directory = models.CharField(max_length=250, null=True, blank=True)

    @classmethod
    def form(cls, *args, **kwargs):
        class YourModelForm(forms.ModelForm):
            class Meta:
                model = cls
                fields = '__all__'
        return YourModelForm
    


 

class Media(models.Model, CoreAttrs):
    file =  models.ImageField(upload_to=generate_filename)
    title = models.CharField(max_length=150, null=True, blank=True)

    @classmethod
    def form(cls, *args, **kwargs):
        class YourModelForm(forms.ModelForm):
            class Meta:
                model = cls
                fields = '__all__'
        return YourModelForm

    class Meta:
        verbose_name = 'Media'
        verbose_name_plural = 'Media'
    def __str__(self) -> str:
        return f"{self.title}"
    
    def list_display(self):
        return ['title','file']
    def list_display_links(self):
        return ['title','file']





class SystemSettings(models.Model, CoreAttrs):
    name = models.CharField(max_length=200)
    context =  models.JSONField()

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'


class SystemSettingLogos(models.Model, CoreAttrs):
    logo = models.ImageField(upload_to='logo')
    favicon = models.ImageField(upload_to='logo')

    class Meta:
        verbose_name = 'Setting Logo'
        verbose_name_plural = 'Settings Logo'

    def form(self):
        from admin_dashboard.forms import SettingsLogosForm
        return SettingsLogosForm
    
    def list_display(self):
        return ['logo','favicon']

    # def save(self, *args, **kwargs) -> None:
    #     # this will prevent multiple registration of data
    #     self._meta.model.objects.all().delete()
    #     return super().save(args, kwargs)