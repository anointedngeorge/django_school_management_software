import importlib
from typing import Any
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

from ..forms.login_form import PluginForm
from ..admin import loadModuleAttribute
from django.template.response import TemplateResponse
from decouple import config
from ..forms import CustomAuthenticationForm as forms
# from ..theme_settings import THEMESETTINGS  as theme_settings

from django.conf import settings
# theme_settings = loadModuleAttribute(app=f"{config('APP_MAIN_NAME')}.theme_settings", attribute='THEMESETTINGS')
# forms = loadModuleAttribute(app=f"{config('APP_MAIN_NAME')}.forms", attribute='CustomAuthenticationForm')
# print(forms)
# from ..plugins.custom_plugins import load_settings
# ts = load_settings(path=config("SETTINGS_JSON_PATH"))
# # print(ts)
ts = settings.GENTELELLA_THEMESETTINGS

class Dashboard2(admin.AdminSite):
    site_header = ts.get("site_header",'Default site header') 
    site_title = ts.get("site_title",'Default site title')
    index_title = ts.get("index_title",'Default index title')
    site_url = ts.get("site_url",'Default site_url')
    login_form =  forms
    template_copyright = ts.get("template_copyright",'&copy; Sharashell')
    footer_title = ts.get("footer_title",'Default footer title')
    site_external_link = ts.get("site_external_link",'Default external link')
    brand_name = ts.get("brand_name",'STL')
    base_uri= ts.get("base_uri",'/')
    theme_logo= ts.get("theme_logo",'')
    theme_favicon_logo= ts.get("theme_favicon_logo",'')
    form_display_size= ts.get("form_display_size",6)
    form_login_title= ts.get("form_login_title",'')
    logout_message= ts.get("logout_message",'')

    def get_urls(self):
            urls = super().get_urls()
            add_urls = [
                path('settings/<str:func_name>/', 
                        self.load_settings,
                    name='settings'),
                    
                path('plugin/<str:id>/<str:function_name>/',
                            self.plugin,
                        name='plugin'),
                ]
            return add_urls + urls
    
    def each_context(self, request: Any) -> Any:
        context = super().each_context(request)
        context['footer_title'] = self.footer_title
        context['template_copyright'] = self.template_copyright
        context['site_external_link'] = self.site_external_link
        context['brand_name'] = self.brand_name
        context['base_uri'] = self.base_uri
        context['theme_logo'] = self.theme_logo
        context['theme_favicon_logo'] = self.theme_favicon_logo
        context['form_display_size'] = self.form_display_size
        context['form_login_title'] = self.form_login_title
        context['logout_message'] = self.logout_message
        context['adminsite'] = self.name
        context['plugin_form'] = PluginForm
        context['main_app_name'] = str(self.__module__).split(".")[0]
        return context


    def load_settings(self, request, func_name=None):
            context = self.each_context(request)
            context['title'] = func_name
            app = context.get("main_app_name")
            '''This module will be used to import all logic related to views'''
            module_name = f'{app}.business_logic.setting_loader'
          
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, func_name):
                    function = getattr(module, func_name)
                    foundFunction = function(request, context)
                    return foundFunction
                else:
                    context['error'] = f"The function {func_name} does not exist in the module."
            except Exception as e:
                context['error'] = e
            return TemplateResponse(request=request, template="admin/404.html", context=context)
    

    def plugin(self, request, id=None, function_name=None, template=None):
        context = self.each_context(request)
        
        # app will print the name of the app_name
        # example dashboard1 or dashboard2, which is stored in the context variable
        app = context.get("main_app_name")
        '''This module will be used to import all logic related to views'''
        module_name = f'{app}.business_logic.plugin'
        query = request.GET.dict()
       
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, function_name):
                function = getattr(module, function_name)
                foundFunction = function(request, id=id, query=query, current_template="")
                return foundFunction
            else:
                context['error'] = f"The function {function_name} does not exist in the module."
        except Exception as e:
            context['error'] = e
        return TemplateResponse(request=request, template="admin/404.html", context=context)
    
# print(config('BASE_APP_NAME'))
SITE_ADMIN1 = Dashboard2(name=f"{config('BASE_APP_NAME')}")



# from django.apps import apps
# mods =  apps.get_models()

# for m in mods:
#     app_name = m.__name__
#     print(m._meta.model.__module__, app_name)


