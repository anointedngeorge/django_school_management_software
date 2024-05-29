import importlib
from django import template
from django.template.loader import render_to_string
from ..models import Plugins
from django.contrib.auth.decorators import permission_required
from ..business_logic import loadModuleAttribute
from django.utils.html import format_html
from decouple import config

register = template.Library()

redirect_path = f"/{config('BASE_APP_NAME')}"

@register.simple_tag
def plugin(request=None, plugin_type="", context={}):
    try:
        context = context
        pl = Plugins.objects.all().filter(plugin_type=plugin_type, status=True)
        if pl.exists():
            found = pl.first()
            templated = render_to_string(
                            template_name=f"{found.template_file}", 
                            context=context, 
                            request=request
                        )
            return templated
        else:
            return ""
    except Exception as e:
        return str(e)



@register.simple_tag
def template_loader(request=None, path='', context={}):
    try:
        context = context
        templated = render_to_string(template_name=path, context=context, request=request)
        return templated
    except Exception as e:
        return str(e)


@register.simple_tag
def show_count(object, **kwargs):
    '''
        Using the importlib to import relative object path.
        this will have some filter arguments from kwargs.
    '''
    try:
        module_name, class_name = object.rsplit('.', 1)
        module = importlib.import_module(module_name)
        app_obj = getattr(module, class_name)
        if len(kwargs) > 0:
            app = app_obj.objects.all().filter(**kwargs)
            return app.count()
        else:
            return app_obj.objects.all().count()
          
    except Exception as e:
        return f"..."
    

@register.simple_tag
def show_filtered_data(object=None, order_by='created', **kwargs):
    if object == None:
        return "Object can not be None."
    try:
        module_name, class_name = object.rsplit('.', 1)
        module = importlib.import_module(module_name)
        app_obj = getattr(module, class_name)
        if len(kwargs) > 0:
            app = app_obj.objects.all().filter(**kwargs).order_by(order_by)
            return app
    except Exception as e:
        return f"{e}"


@register.simple_tag
def show_data_list(object=None, limit=6, order_by='created' ):
    try:
        module_name, class_name = object.rsplit('.', 1)
        module = importlib.import_module(module_name)
        app_obj = getattr(module, class_name)
        app = app_obj.objects.all().order_by(order_by)
        app = app[:limit]
        return app
    except Exception as e:
        return f"{e}"
    


@register.filter
def main_bootstrap_form(form_list):
    table_html = ''
    table_html += '<div class="row">'
    for f in form_list:
        table_html += f'<div class="col-lg-4">'
        table_html += f'{f.label_tag()}'
        table_html += f"{f}"
        table_html += '</div>'
    table_html += '</div>'
    return format_html(table_html)