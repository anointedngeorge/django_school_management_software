import importlib
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
from admin_dashboard.views.functions import check_user, PAGE_NOT_FOUND,admin_custom_permission_required

BRANCH_BASE_DIR_NAME = "admin_custom/"
PRODUCT_APP_NAMESPACE = "admin_dashboard"
LOGIN_URL = f'/{BRANCH_BASE_DIR_NAME}/'
PRODUCT_LOGIN_NAMESPACE = f"{PRODUCT_APP_NAMESPACE}:login"


class ChangeFormFunc(TemplateView):
    """For creat a new form data """
    template_name = f"{BRANCH_BASE_DIR_NAME}/change_form.html"

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
        context = super().get_context_data(**kwargs)
        try:
            userid = self.request.user.pk
            appname = kwargs.get("appname")
            modelname = kwargs.get("modelname")
            importedapp = self.import_by_name(appname, modelname)

            if hasattr(importedapp, modelname):
                obj = getattr(importedapp, modelname)
                context['object'] = obj
                context['action_title'] = str(modelname).upper()
                context['modelname'] = modelname
                context['appname'] = appname
                context['page_title'] = f"{appname} - {modelname}".title()
            
        except Exception as e:
            return context
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            
            appname = kwargs.get("appname")
            modelname = kwargs.get("modelname")
            importedapp = self.import_by_name(appname, modelname)

            if hasattr(importedapp, modelname):
                obj = getattr(importedapp, modelname)
                # check if the form contains files
                fm = obj.form()(request.POST) if bool(request.FILES) == False else obj.form()(request.POST, request.FILES)
                if fm.is_valid():
                    fm.save()
                    django_message.success(request, f"{modelname} {ErrorMessages.FORM_ON_SUCCESS}")
                else:
                    django_message.error(request, f"{modelname} {ErrorMessages.FORM_ON_FAILED}")
            return redirect(request.META.get("HTTP_REFERER"))
    
        except Exception as e:
            django_message.error(request, f"{e} > {ErrorMessages.FORM_ON_ERROR}")
            return redirect(request.META.get("HTTP_REFERER"))




# for modal form display
        
class ModalChangeFormFunc(TemplateView):
    """For creat a new form data """
    template_name = f"{BRANCH_BASE_DIR_NAME}/modal_change_form.html"

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
        context = super().get_context_data(**kwargs)
        try:
            userid = self.request.user.pk
            appname = kwargs.get("appname")
            modelname = kwargs.get("modelname")
            importedapp = self.import_by_name(appname, modelname)
            context['add'] = False
            context['list'] = True
            if hasattr(importedapp, modelname):
                obj = getattr(importedapp, modelname)
                context['object'] = obj
                context['action_title'] = str(modelname).upper()
                context['modelname'] = modelname
                context['appname'] = appname
            
        except Exception as e:
            return context
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            
            appname = kwargs.get("appname")
            modelname = kwargs.get("modelname")
            importedapp = self.import_by_name(appname, modelname)

            if hasattr(importedapp, modelname):
                obj = getattr(importedapp, modelname)
                # check if the form contains files
                fm = obj.form(self)(request.POST) if bool(request.FILES) == False else obj.form(self)(request.POST, request.FILES)
                if fm.is_valid():
                    fm.save()
                    django_message.success(request, f"{modelname} {ErrorMessages.FORM_ON_SUCCESS}")
                else:
                    django_message.error(request, f"{modelname} {ErrorMessages.FORM_ON_FAILED}")
            return redirect(request.META.get("HTTP_REFERER"))
    
        except Exception as e:
            django_message.error(request, f"{e} > {ErrorMessages.FORM_ON_ERROR}")
            return redirect(request.META.get("HTTP_REFERER"))

    







    

class UpdateFormFunc(TemplateView):
    """For change form """
    template_name = f"{BRANCH_BASE_DIR_NAME}/update_change_form.html"

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
        context = super().get_context_data(**kwargs)
        try:
            
            objectid = kwargs.get("objectid")
            appname = kwargs.get("appname")
            modelname = kwargs.get("modelname")
            importedapp = self.import_by_name(appname, modelname)
        

            if hasattr(importedapp, modelname):
                obj = getattr(importedapp, modelname)
                context['object'] = obj
                context['model'] = obj.objects.all()
                context['action_title'] = str(modelname).upper()
                context['modelname'] = modelname
                context['appname'] = appname
                context['objectid'] = objectid
                context['page_title'] = f"{appname} - {modelname}".title()
            
        except Exception as e:
            return context
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            objectid = kwargs.get("objectid")
            appname = kwargs.get("appname")
            modelname = kwargs.get("modelname")
            importedapp = self.import_by_name(appname, modelname)

            if hasattr(importedapp, modelname):
                obj = getattr(importedapp, modelname)
                m =  obj.objects.all().filter(id=objectid).get()
                
                fm = obj.form()(request.POST, instance=m) if bool(request.FILES) == False else obj.form()(request.POST, request.FILES, instance=m)
                if fm.is_valid():
                    fm.save()
                    django_message.success(request, f"{modelname} Updated.")
                else:
                    django_message.error(request, f"{modelname} failed to create.")
            return redirect(request.META.get("HTTP_REFERER"))
        except Exception as e:
            import traceback
            traceback.print_exc()
            return redirect(request.META.get("HTTP_REFERER"))




def import_by_name(appname, modelname):
        try:
            imported_module = importlib.import_module(f"{appname}.models")
            return imported_module
        except ImportError as e:
            return None

@login_required(login_url=reverse_lazy(PRODUCT_APP_NAMESPACE))
@admin_custom_permission_required
def DeleteChangeListObject(request, **kwargs): 
    try:
        objectid = kwargs.get("objectid")
        appname = kwargs.get("appname")
        modelname = kwargs.get("modelname")
        importedapp = import_by_name(appname, modelname)

        if hasattr(importedapp, modelname):
            obj = getattr(importedapp, modelname)
            m =  obj.objects.all().filter(id=objectid)
            if m.exists():
                m.delete()
            django_message.success(request, "Item Removed")
            url = reverse('admin_dashboard:changelist', kwargs={'appname':appname, 'modelname':modelname})
            return redirect(url)
    except Exception as e:
        django_message.error(request, f"{e}")
        return redirect("admin_dashboard:dashboard")



