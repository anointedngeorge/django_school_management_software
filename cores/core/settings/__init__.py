from decouple import config


if config('ENVIRONMENT') == 'production':
    from core.settings.prod_settings import *

elif config('ENVIRONMENT') == 'development':
    from core.settings.dev_settings import *