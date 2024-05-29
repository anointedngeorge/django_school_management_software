from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseForbidden
from django.urls import reverse
from schools.models import Schools

class TenantActivationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            tenant = request.tenant
            if not tenant.is_active:
                message = f'''
                    Dear ({tenant}), your acount has been suspended. Please contact you administrator.
                    '''
                return HttpResponseForbidden(str(message).upper())
            return None
        except:
            pass
