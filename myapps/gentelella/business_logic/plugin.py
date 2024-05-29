from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.contrib import messages as msg
import os
import shutil
from decouple import config
from ..business_logic import loadModuleAttribute
from ..models import Plugins

# Plugins = loadModuleAttribute(f"{config('APP_MAIN_NAME')}.models", 'Plugins')
redirect_path = f"/{config('BASE_APP_NAME')}"

def activate(request, id=None, query={}, current_template=""):
    try:
        context = {}
        
        context['query'] = query
        context['id'] = id
        kwargs = {"status":int(query.get("status"))}
        type = query.get('type',None)
        # 
        plugins_to_update = Plugins.objects.filter(plugin_type=type)
        plugins_to_update.update(status=False)
        # 
        Plugins.objects.all().filter(id=int(id)).update(**kwargs)
        msg.success(request, "Plugin Activated")
        return redirect(redirect_path)
    except Exception as e:
        return str(e)
    


def deactivate(request, id=None, query={}, current_template=""):
    try:
        context = {}
        context['query'] = query
        context['id'] = id
        kwargs = {"status":int(query.get("status"))}
        Plugins.objects.all().filter(id=int(id)).update(**kwargs)
        msg.info(request, "Plugin Deactivated")
        return redirect(redirect_path)
    except Exception as e:
        return str(e)


def delete(request, id=None, query={}, current_template=""):
    try:
        context = {}
        context['query'] = query
        context['id'] = id
        found = Plugins.objects.all().filter(id=int(id))
        if found.exists():
            found2 = found.first()
            # found2.delete()
            if os.path.exists(found2.directory):
               shutil.rmtree(f"{found2.directory}")
               found.delete()
        msg.info(request, "Plugin Deleted")
        return redirect(redirect_path)
    except Exception as e:
        return str(e)