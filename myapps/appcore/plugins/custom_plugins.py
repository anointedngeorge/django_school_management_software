from decouple import config
from django.utils.html import format_html
from django.template.loader import render_to_string
import importlib
import os
import uuid
# from django.


def BASE_URI(pattern=''):
    BASE_APP_NAME =  config("BASE_APP_NAME")
    return f"/{BASE_APP_NAME}/{pattern}"


def dropdown(template_name='',context={}, app_module=""):
    try:
        context['app'] = f"{app_module}/pages/"
        html = render_to_string(
            template_name=f"{template_name}",
            context=context
        )
        return html
    except Exception as e:
        return str(e)


def actionparam(
        title='',
        url='',
        has_modal=False,
        is_active=True,
        classicon='',
        permission='',
        query={}
    ):
    return dict({
        'title':title,
        'url':url,
        'has_modal':has_modal,
        'is_active':is_active,
        'classicon':classicon,
        'permission':permission,
        'query':query
    })


def param(
        title='',
        url='',
        has_modal=False,
        is_active=True,
        classicon='',
        query={}
    ):
    return dict({
        'title':title,
        'url':url,
        'has_modal':has_modal,
        'is_active':is_active,
        'classicon':classicon,
        'query':query
    })



def word_to_underscore(string):
    import re
    # Match words separated by spaces, hyphens, or plus/minus signs
    pattern = r'[\s\-+]+'
    # Replace matched patterns with underscores
    output_string = re.sub(pattern, '_', string)
    return output_string


def loadModuleAttribute(app, attribute):
    module =  importlib.import_module(app)
    foundapi = getattr(module,attribute)
    return foundapi

def loadModule(app):
    module =  importlib.import_module(app)
    return module


def generate_filename(instance, filename):
    # Generate a unique filename using a UUID
    filename = str(uuid.uuid4()) + os.path.splitext(filename)[1]
    # Return the path where the file should be uploaded
    return os.path.join('photo', filename)



def load_settings(path = ""):
    try:
        import json

        # print(type(st.first().settings))
        if os.path.exists(path):
            
            with open(os.path.realpath(path), 'r') as file :
                data = json.load(file)
                return data
        else:
            return {}
    except Exception as e:
        return f"{e}"