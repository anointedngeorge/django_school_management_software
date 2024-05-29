import importlib
import json
from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from coreattrs.user_permissions_context import UserPermissions
from django.contrib import messages as django_message
from typing import List
from coreattrs.error_messages import ErrorMessages
from appcore.models import SystemSettings
from admin_dashboard.views.functions import check_user, PAGE_NOT_FOUND, admin_custom_permission_required

BRANCH_BASE_DIR_NAME = "admin_custom/"
PRODUCT_APP_NAMESPACE = "admin_dashboard"
LOGIN_URL = f'/{BRANCH_BASE_DIR_NAME}/'
PRODUCT_LOGIN_NAMESPACE = f"{PRODUCT_APP_NAMESPACE}:login"


class SettingsFun(TemplateView):
    """For creat a new form data """
    template_name = f"{BRANCH_BASE_DIR_NAME}/settings/settings.html"
    setting_name="settingname"

    @method_decorator(login_required(login_url=reverse_lazy(PRODUCT_LOGIN_NAMESPACE)))
    @method_decorator(admin_custom_permission_required)
    def dispatch(self, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(self.request, *args, **kwargs)
    
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from admin_dashboard.forms import SettingsForm, TemplateSettingsForm
        try:
            name = kwargs.get('name','settingname')
         
            if name == 'settingname':
                context['page_title'] = "General Settings"
                context['form'] = SettingsForm(setting_name=name )
            elif name == 'templatetext':
                context['page_title'] = "Template Text Settings"
                context['form'] = TemplateSettingsForm(setting_name=name )
        except Exception as e:
            return context
        context['name'] = name
        return context

    
    def post(self, request, *args, **kwargs):
        try:
            name = kwargs.get('name','name')

            data_model = SystemSettings.objects.all()
            dataform = request.POST.dict()
            
            dataform.pop('csrfmiddlewaretoken')
            if data_model.filter(name=name).exists():
                data_model.filter(name=name).update(context=dataform)
                django_message.info(request, f"Settings Updated")
            else:
                data_model.create(name=name, context=dataform)
                django_message.success(request, f"Create new settings")
            return redirect(request.META.get("HTTP_REFERER"))
    
        except Exception as e:
            django_message.error(request, f"{e} > {ErrorMessages.FORM_ON_ERROR}")
            return redirect(request.META.get("HTTP_REFERER"))

        
