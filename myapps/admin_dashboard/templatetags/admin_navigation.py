import importlib
from django.utils.html import format_html
from django import template
from decouple import config
import requests
from admin_dashboard.NAVIGATION_LINKS import NAVIGATION_LINKS
from admin_dashboard.plugins.code_generator import shufflerWithoutInt
register = template.Library()



@register.inclusion_tag("admin_custom/app_list.html", takes_context=True)
def navigations(context):
    context = {
        "navigations": NAVIGATION_LINKS
    }
    return context


@register.simple_tag
def randomize(size=8, step=1):
    sh = shufflerWithoutInt(size=size, step=step)
    sf = "".join(str(sh))
    return sf