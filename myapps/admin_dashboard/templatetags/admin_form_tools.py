import importlib
from django import template
from django.template.loader import render_to_string
from appcore.models import Plugins
from django.contrib.auth.decorators import permission_required
from functools import reduce
import operator
import traceback

register = template.Library()


@register.filter
def is_foreign_key_or_m2m(field):
    """
    Check if the given form field represents a ForeignKey or ManyToManyField.
    """
    format_url = ""
    name = field.field
    check = name.__class__.__name__ in ['ModelChoiceField', 'ModelMultipleChoiceField']
    return check



@register.simple_tag
def foreign_key_or_m2m(field):
    context = {}
    name = field.field
    check = name.__class__.__name__ in ['ModelChoiceField', 'ModelMultipleChoiceField']
    if check:
        model_class = field.field.queryset.model
        appname = f"{model_class.__module__}".split('.')[0]
        modelname =  model_class.__name__
        context['appname'] = appname
        context['modelname'] = modelname
        
    return context







