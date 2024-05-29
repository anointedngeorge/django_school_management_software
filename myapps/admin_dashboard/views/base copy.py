from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from coreattrs.user_permissions_context import UserPermissions
from django.contrib import messages as django_message
from ..forms import LoginForm
from typing import List
from coreattrs.error_messages import ErrorMessages
from admin_dashboard.views.functions import check_user, PAGE_NOT_FOUND, admin_custom_permission_required
from django.apps import apps

BASE_DIR_NAME = "admin_custom"
APP_NAMESPACE = "admin_dashboard"
LOGIN_URL = f'/{BASE_DIR_NAME}/'
LOGIN_NAMESPACE = f"{APP_NAMESPACE}:login"


class LoginFunc(TemplateView):
    template_name = f"{BASE_DIR_NAME}/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LoginForm
        context['LOGIN_TITLE'] = "Admin Dashboard"
        context['page_title'] = "Login Page"
        return context

    def post(self, request, *args, **kwargs):
        try:
            post_data = LoginForm(request.POST)
            # print(post_data )

            if post_data.is_valid():
                username =  post_data.cleaned_data.get("username")
                password = post_data.cleaned_data.get("password")  
                user = authenticate(request=self.request, username=username, password=password)
                
                if user != None:
                    login(user=user, request=request)
                    return redirect(f"{APP_NAMESPACE}:dashboard")
                else:
                    django_message.error(request, f"{ErrorMessages.LOGIN_ACCOUNT_ACTIVATION_MESSAGE}")
                    return redirect(f"{APP_NAMESPACE}:login")

            else:
                django_message.error(request, f"{post_data.error_messages}")
                url = reverse(f"{APP_NAMESPACE}:login", kwargs={})
                return HttpResponseRedirect(redirect_to=url)
        except Exception as e:
            return HttpResponse(e)



class Dashboard(TemplateView): 
    template_name = f"{BASE_DIR_NAME}/index.html"

    @method_decorator(login_required(login_url=reverse_lazy(LOGIN_NAMESPACE)))
    @method_decorator(admin_custom_permission_required)
    def dispatch(self, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        # Add additional context data if needed
        return context



class ProfileFunc(TemplateView):
    """For users profile """
    template_name = f"{BASE_DIR_NAME}/profile.html"

    @method_decorator(login_required(login_url=reverse_lazy(LOGIN_NAMESPACE)))
    @method_decorator(admin_custom_permission_required)
    def dispatch(self, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(self.request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.user.pk
        return context




class MessageFunc(TemplateView):
    """For users messages """
    template_name = f"{BASE_DIR_NAME}/messages.html"

    @method_decorator(login_required(login_url=reverse_lazy(LOGIN_NAMESPACE)))
    @method_decorator(admin_custom_permission_required)
    def dispatch(self, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(self.request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.user.pk
        return context


@login_required(login_url=reverse_lazy(LOGIN_NAMESPACE))
def logoutFunc(request): 
    logout(request)
    return redirect(f"{APP_NAMESPACE}:login")