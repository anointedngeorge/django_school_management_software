import importlib
from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from coreattrs.user_permissions_context import UserPermissions
from django.contrib import messages as django_message
from typing import List
from admin_dashboard.views.functions import check_user, PAGE_NOT_FOUND, admin_custom_permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


BRANCH_BASE_DIR_NAME = "admin_custom/"
PRODUCT_APP_NAMESPACE = "admin_dashboard"
LOGIN_URL = f'/{BRANCH_BASE_DIR_NAME}/'
PRODUCT_LOGIN_NAMESPACE = f"{PRODUCT_APP_NAMESPACE}:login"




class ChangeListFunc(TemplateView):
    """For change list """
    template_name = f"{BRANCH_BASE_DIR_NAME}/change_list.html"

    @method_decorator(login_required(login_url=reverse_lazy(PRODUCT_LOGIN_NAMESPACE)))
    @method_decorator(admin_custom_permission_required)
    def dispatch(self, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(self.request, *args, **kwargs)
    
    def import_by_name(self, appname, modelname):
        try:
            imported_module = importlib.import_module(f"{appname}.models")
            return imported_module
        except ImportError as e:
            return None

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            userid = self.request.user.pk
            appname = kwargs.get("appname")
            modelname = kwargs.get("modelname")
            importedapp = self.import_by_name(appname, modelname)

            if hasattr(importedapp, modelname):
                obj = getattr(importedapp, modelname)
                ordering_str = ""

                ordering = obj._meta.ordering
                if len(ordering) > 0:
                    ordering_str = ",".join(ordering)
                    
                else:
                    ordering_str = "id"
                paginator = Paginator(obj.objects.all().order_by(ordering_str), 10)

                page = self.request.GET.get('page')
                
                try:
                    objects = paginator.page(page)
                    
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    objects = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    objects = paginator.page(paginator.num_pages)
                    
            
                # object_list = objects
                context['object_list'] = objects
                context['object'] = obj
                context['action_title'] = str(modelname).upper()
                context['appname'] = appname
                context['modelname'] = modelname
                context['page_title'] = f"{appname} - {modelname}".title()
            else:
                raise Http404("Not found")
            return context
        except:
            pass
    
