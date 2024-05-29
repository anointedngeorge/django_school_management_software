from typing import Iterable
from django.db import models

from .plugins.custom_plugins import generate_filename

from .icons import ICONS
from decouple import config
from .core_attrs import CoreAttrs
from .actions.custom_action1 import change_url
from user_permissions_context import UserPermissions


MAIN_DASHBOARD = "gentelella"

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


class ChildrenMenus(models.Model,CoreAttrs):
    icon = models.CharField(max_length=150, null=True, blank=True, choices=ICONS)
    title = models.CharField(max_length=150, null=True, blank=True)
    url = models.CharField(max_length=150, default=f"/{config('BASE_APP_NAME')}")

    def __str__(self) -> str:
        return f"Menus {self.title}"
    
    class Meta:
        verbose_name = 'Children Menu'
        verbose_name_plural = 'Children Menus'

    def list_display(self):
        return ['icon','title','url']
    def list_display_links(self):
        return ['icon','title']
    def has_action(self):
        return True
    def action(self):
        return [change_url, "delete_selected"]

class Menus(models.Model, CoreAttrs):

    menu_type = models.CharField(max_length=150, choices=[
        ('menu','Menu'),
        ('top_menu','Top Menu')
    ], default='menu')

    permission = models.CharField(max_length=150, choices=UserPermissions.choices, null=True)
    icon = models.CharField(max_length=150, null=True, blank=True, choices=ICONS)
    title = models.CharField(max_length=150, null=True, blank=True)
    url = models.CharField(max_length=150, default=f"/{config('BASE_APP_NAME')}")
    has_children = models.BooleanField(default=False, choices=[(False,"No"), (True,"Yes")])
    is_allowed = models.BooleanField(default=False, choices=[(False,"No"), (True,"Yes")])
    order = models.IntegerField(default=1)
    children_links=models.ManyToManyField(ChildrenMenus, blank=True, related_name="children_menus")
    

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'

    def __str__(self) -> str:
        return f"Menus {self.title}"
    
    def _permission(self):
        if self.permission != None:
            return f"To {self.permission}"
        else:
            return "To Admin"
    
    def list_display(self):
        return ['_permission','menu_type','icon','title','has_children','is_allowed','order','url']
    
    def list_filter(self):
        return ['title','is_allowed']
    def has_action(self):
        return True
    def action(self):
        return [change_url, "delete_selected"]
    
    @property
    def children(self):
        try:
            cont = []
            obj =  self.children_links.all()
            for x in obj:
                cont.append({'title':x.title,'icon':x.icon,'url':x.url})
            return cont
        except Exception as e:
            pass
        return []
    

class Media(models.Model, CoreAttrs):
    file =  models.ImageField(upload_to=generate_filename)
    title = models.CharField(max_length=150, null=True, blank=True)

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
    settings = models.JSONField(null=True)

    def __str__(self) -> str:
        return f"system settings"
    
    def list_display(self):
        return ['settings']

 