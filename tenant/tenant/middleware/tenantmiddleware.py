from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseForbidden
from django.urls import reverse
from schools.models import Schools
import re

class TenantActivationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Allow access to the /admin/ path
        
        expression = re.search(r'admin/', request.path)
        
        if expression:
            return None

        else:
            tenant = request.tenant
            if not tenant.is_active:
                message = f'''
                    Dear ({tenant}), your account has been suspended. Please contact your administrator.
                    '''
                return HttpResponseForbidden(str(message).upper())
        
        return None
