import importlib
from django.utils.html import format_html
from django import template
from decouple import config
import requests

register = template.Library()

def requestdata(url=''):
    try:
        dt =  requests.get(f"{config('MAIN_URL')}/{url}")
        if dt.ok:
            return dt.json()
        else:
            return {}
    except Exception as e:
        return e
    

@register.inclusion_tag(
                    filename="admin/app_list.html", 
                    takes_context=True,
                    )
def navigation_inclusion_tag(context, request=None, object=None, menu='menu'):
    module = importlib.import_module(object)
    NAV_MAP = getattr(module, "Menus")
    obj =  NAV_MAP.objects.all().filter(menu_type=menu).order_by("order")

    context = {
        "navigation":obj,
        "request":request
    }
    return context


@register.simple_tag
def navigation_without_inclusion_tag(request=None, object=None, menu='menu'):
    module = importlib.import_module(object)
    NAV_MAP = getattr(module, "Menus")
    obj =  NAV_MAP.objects.all().filter(menu_type=menu).order_by("order")

    context = {
        "navigation":obj,
        "request":request
    }
    return context


@register.simple_tag
def splituri(url=''):
    try:
        splitted = str(url).rsplit("/")
        if len(splitted) > 0:
            # remove empty strings
            formatted = [x for x in splitted if x !=""]
            join_formatted = "/".join(formatted[:2])
            return "/"+join_formatted
        return ""
    except Exception as e:
        return str(e)

@register.simple_tag
def query(q={}):
    try:
        if isinstance(q,dict):
            # string comprehension to form query get params
            query = "&".join(f"{key}={value}" for key,value in q.items())
            return query
        return f"{q} is a vaild python dict!"
    except Exception as e:
        return str(e)
    

@register.simple_tag
def settings_url(title='Plugins', anchor='plugins', icon='fa fa-upload', is_allowed=False):
    try:
        if not is_allowed:
            return ""
        url = f" <a href='/{config('BASE_APP_NAME')}/{anchor}'><i class='{icon}'></i> {title}</a>"
        return format_html(url)
    except:
        return ''


@register.simple_tag
def menus_url(title='Menus', icon='fa fa-upload',is_allowed=False):
    try:
        if not is_allowed:
            return ""
        url = f" <a href='/{config('BASE_APP_NAME')}/{config('APP_MAIN_NAME')}/menus'><i class='{icon}'></i> {title}</a>"
        return format_html(url)
    except:
        return