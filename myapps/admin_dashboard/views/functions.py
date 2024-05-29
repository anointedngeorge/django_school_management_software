from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from functools import wraps

PAGE_NOT_FOUND = "admin_custom/error/403.html"

def check_user(user):
    return False



def admin_custom_permission_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return render(request=request, template_name=PAGE_NOT_FOUND, status=403)
        return view_func(request, *args, **kwargs)
    return wrapper