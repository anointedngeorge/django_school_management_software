
import importlib

def loadModuleAttribute(app, attribute):
    try:
        module =  importlib.import_module(app)
        if hasattr(module,attribute):
            found = getattr(module,attribute)
            return found
        return ""
    except Exception as e:
        return str(e)