from django.template.response import TemplateResponse
from django.http import HttpResponse
from decouple import config

from ..admin import loadModuleAttribute

# Plugins = loadModuleAttribute(f"{config('APP_MAIN_NAME')}.models", 'Plugins')
# redirect_path = f"/{config('BASE_APP_NAME')}"

def viewprofile(request, id, query, current_template):
    try:
        context = {}
        context['query'] = query
        context['id'] = id
        return TemplateResponse(
            request=request,
            template="admin/templateresponse/view_profile.html",
            context=context,
            status=200,
        )
    except Exception as e:
        return str(e)