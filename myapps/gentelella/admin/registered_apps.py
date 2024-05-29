import os
import importlib
import shutil
from typing import List
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import URLResolver, path
from django.template.response import TemplateResponse
from decouple import config

from ..admin.base import SITE_ADMIN1
from ..admin.custom_apps import REGISTERED_APP
from ..admin import loadModuleAttribute

# load app dynamically using loadModuleAttribute function, for dynamic import

# SITE_ADMIN1 = loadModuleAttribute(f"{config('APP_MAIN_NAME')}.admin.base","SITE_ADMIN1")
# REGISTERED_APP = loadModuleAttribute(f"{config('APP_MAIN_NAME')}.admin.custom_apps","REGISTERED_APP")

# 
try:
    for app in REGISTERED_APP:
        module_name, class_name = app.rsplit('.', 1)
        
        module = importlib.import_module(module_name)
        app_obj = getattr(module, class_name)

        list_display = app_obj.list_display(None) if hasattr(app_obj,"list_display") else ['pk']
        list_filter = app_obj.list_filter(None) if hasattr(app_obj,"list_filter") else []
        list_display_links = app_obj.list_display_links(None) if hasattr(app_obj,"list_display_links") else ['pk']
        exclude = app_obj.exclude(None) if hasattr(app_obj,"exclude") else []
        has_action = app_obj.has_action(None) if hasattr(app_obj,"has_action") else False
        actions = app_obj.action(None) if hasattr(app_obj,"action") else []
        has_dropdown_action = app_obj.has_dropdown_action(None) if hasattr(app_obj,"has_dropdown_action") else False
        dropdown_action = app_obj.dropdown_action(None) if hasattr(app_obj,"dropdown_action") else []
        is_registered = app_obj.is_registered(None) if hasattr(app_obj,"is_registered") else False
        

        form_app =  False

        if is_registered:

            class RegisteredAPPS(admin.ModelAdmin):
                list_display = list_display
                list_display_links = list_display_links
                list_filter = list_filter
                actions = actions
                exclude = exclude
                app_class_name = app_obj._meta
                extra_forms = app_obj.extra_forms(None) if hasattr(app_obj,"extra_forms") else dict
                
                if ((hasattr(app_obj,"form")) and (app_obj.form(None) != None)):
                    form = app_obj.form(None)
              
                def get_urls(self):
                    urls = super().get_urls()
              
                    add_urls = [
                            path('view/<str:id>/<str:function_name>/', 
                                self.admin_site.admin_view(self.views),
                                name='view'),

                            path('view/<str:function_name>/', 
                                self.admin_site.admin_view(self.views),
                                name='view'),

                            path('create/<str:id>/<str:function_name>/', 
                             self.admin_site.admin_view(self.create),
                            name='create'),
                        ]
                    return add_urls + urls
                
                def response_delete(self, request: HttpRequest, obj_display=None, obj_id=None) -> HttpResponse:
                    try:
                        m_name = self.model.__name__
                        if m_name == "Media":
                            modl = self.model.objects.all().filter(id=obj_id)
                            print(modl)
                            print(obj_display, obj_id, m_name)
                    except Exception as e:
                        print(e)
                    return super().response_delete(request, obj_display, obj_id)

                # def changeform_view(self, request, object_id=None, form_url=None, extra_context=None):
                #     extra_context = extra_context or {}
                    
                #     try:
                #         if self.extra_forms != None:
                #             f = self.extra_forms.get("form")
                #             extra_context['editstudentformresult'] = f(object_id=object_id) if f else dict
                #     except Exception as e:
                #         pass
                #     return super().changeform_view(request, object_id, form_url, extra_context)
                
                def each_context(self, request):
                    context = SITE_ADMIN1.each_context(request)
                    
                    return context
                
                def views(self, request, id=None, function_name=None, template=None):
                    context = self.each_context(request)
                    app_module =  str(self.model._meta).split(".")[0]
                    # print("Page listening...", function_name, app_module)
                    # app will print the name of the app_name
                    # example dashboard1 or dashboard2, which is stored in the context variable
                    app = context.get("main_app_name")
                    '''This module will be used to import all logic related to views'''

                    module_name = f'{app}.business_logic.view'
                    module_name1 = f'{app_module}.business_logic.view'
                    query = request.GET.dict()
                    
                    try:
                        if hasattr(importlib.import_module(module_name), function_name):
                            module = importlib.import_module(module_name)
                            function = getattr(module, function_name)
                            foundFunction = function(request, id=id, query=query, context=context)
                            return foundFunction
                        
                        elif hasattr(importlib.import_module(module_name1), function_name):
                            module = importlib.import_module(module_name1)
                            function = getattr(module, function_name)
                            foundFunction = function(request, id=id, query=query, context=context)
                            return foundFunction
                        else:
                            context['error'] = f"The function {function_name} in {app_module} does not exist in the module."
                    
                    except Exception as e:
                        context['error'] = e
                    return TemplateResponse(request=request, template="admin/404.html", context=context)
                


                def create(self, request, id=None, function_name=None, template=None):
                    context = self.each_context(request)
                    app_module =  str(self.model._meta).split(".")[0]

                    # app will print the name of the app_name
                    # example dashboard1 or dashboard2, which is stored in the context variable
                    app = context.get("main_app_name")
                    '''This module will be used to import all logic related to views'''

                    module_name = f'{app}.business_logic.create'
                    module_name1 = f'{app_module}.business_logic.create'
                    query = request.GET.dict()
                    
                    try:
                        if hasattr(importlib.import_module(module_name), function_name):
                            module = importlib.import_module(module_name)
                            function = getattr(module, function_name)
                            foundFunction = function(request, id=id, query=query, context=context)
                            return foundFunction
                        
                        elif hasattr(importlib.import_module(module_name1), function_name):
                            module = importlib.import_module(module_name1)
                            function = getattr(module, function_name)
                            foundFunction = function(request, id=id, query=query, context=context)
                            return foundFunction
                        else:
                            context['error'] = f"The function {function_name} in {app_module} does not exist in the module."
                    
                    except Exception as e:
                        context['error'] = e
                    return TemplateResponse(request=request, template="admin/404.html", context=context)
                
            SITE_ADMIN1.register(app_obj, RegisteredAPPS)
            
except Exception as e:
    pass