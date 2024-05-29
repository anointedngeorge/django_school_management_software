from django.apps import apps

REGISTERED_APP = []

mods =  apps.get_models()
for m in mods:
    model_name = m.__name__
    module = f"{m._meta.model.__module__}.{model_name}"
    REGISTERED_APP.append(module)
   