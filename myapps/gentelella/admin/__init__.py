import importlib
from decouple import config

def loadModuleAttribute(app, attribute):
    try:
        module =  importlib.import_module(app)
        if hasattr(module,attribute):
            found = getattr(module,attribute)
            return found
        return ""
    except Exception as e:
        print(e)
        return str(e)

# load all apps with this line
loadModuleAttribute(f"{config('APP_MAIN_NAME')}.admin.registered_apps","*")