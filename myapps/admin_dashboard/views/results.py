from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic import RedirectView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from coreattrs.user_permissions_context import UserPermissions
from django.contrib import messages as django_message

from myschool.forms.result_form import PrintResultForm
from ..forms import LoginForm
from typing import List
from coreattrs.error_messages import ErrorMessages
from admin_dashboard.views.functions import check_user, PAGE_NOT_FOUND, admin_custom_permission_required
from django.apps import apps
from urllib.parse import urlencode
# load business logic


BASE_DIR_NAME = "admin_custom"
APP_NAMESPACE = "admin_dashboard"
LOGIN_URL = f'/{BASE_DIR_NAME}/'
LOGIN_NAMESPACE = f"{APP_NAMESPACE}:login"
ON_SUCCESS_URL = f"{APP_NAMESPACE}:redirect_url"



class AddNewResult(TemplateView): 
    template_name = f"{BASE_DIR_NAME}/results/add_results.html"

    @method_decorator(login_required(login_url=reverse_lazy(LOGIN_NAMESPACE)))
    @method_decorator(admin_custom_permission_required)
    def dispatch(self, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
 
        context['page_title'] = f"New Result".title()
        # Add additional context data if needed
        return context
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        from admin_dashboard.views.business_logic.view import result_load_student
        # return super().get(request, *args, **kwargs)
        return result_load_student(request=self.request, id=None, query=kwargs, context={})


@login_required(login_url=reverse_lazy(LOGIN_NAMESPACE))
def completeResultUpload(request, *args, **kwargs):
    query = request.GET.dict()
    from admin_dashboard.views.business_logic.view import loadResultform
        # return super().get(request, *args, **kwargs)
    return loadResultform(request=request, id=None, query=query, context={})


@login_required(login_url=reverse_lazy(LOGIN_NAMESPACE))
def updateUploadResult(request, *args, **kwargs):
    query = request.GET.dict()
    from admin_dashboard.views.business_logic.view import updateResultform
        # return super().get(request, *args, **kwargs)
    return updateResultform(request=request, id=None, query=query, context={})



class PrintResults(TemplateView): 
    template_name = f"{BASE_DIR_NAME}/results/result_printing_page.html"

    @method_decorator(login_required(login_url=reverse_lazy(LOGIN_NAMESPACE)))
    @method_decorator(admin_custom_permission_required)
    def dispatch(self, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['form'] = PrintResultForm
        context['page_title'] = f"Print Results".title()
        return context

    def post(self, *args, **kwargs):
        from admin_dashboard.views.business_logic.view import printresult
        return printresult(request=self.request, id=None, query={}, context={})

class EditNewResult(TemplateView): 
    template_name = f"{BASE_DIR_NAME}/results/edit_results.html"

    @method_decorator(login_required(login_url=reverse_lazy(LOGIN_NAMESPACE)))
    @method_decorator(admin_custom_permission_required)
    def dispatch(self, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(self.request, *args, **kwargs)
    
    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit Results".title()
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        from admin_dashboard.views.business_logic.view import result_edit_student
        # return super().get(request, *args, **kwargs)
        return result_edit_student(request=self.request, id=None, query=kwargs, context={})

