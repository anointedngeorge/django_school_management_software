from decouple import config


if config('ENVIRONMENT') == 'production':
    from tenant.settings.prod_settings import *

elif config('ENVIRONMENT') == 'development':
    from tenant.settings.dev_settings import *