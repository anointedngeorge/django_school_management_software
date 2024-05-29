import importlib

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