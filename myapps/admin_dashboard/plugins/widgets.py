from pathlib import Path
import os
import sys
import importlib

# import folder directory
BASE_DIR = Path(__file__).resolve().parent.parent


def load_directory_contents(path=''):
    try:
        file_path = os.path.join(BASE_DIR, path)
        if os.path.exists(file_path):
            list_directory = os.listdir(file_path)
            container = [(x, str(x).split('.')[0]) for x in list_directory]
            return container
        else:
            return
    except Exception as e:
        return [(None, str(e))]
    

def get_data(object=None, **kwargs):
    if object == None:
        return "Object is object."
    try:
        module_name, class_name = object.rsplit('.', 1)
        module = importlib.import_module(module_name)
        app_obj = getattr(module, class_name)
        if len(kwargs) > 0:
            app = app_obj.objects.all().filter(**kwargs).first()
            if app:
                return app.context
            else:
                return 'default'
    except Exception as e:
        return {"none": e}