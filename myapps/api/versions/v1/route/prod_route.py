import datetime
from ninja import NinjaAPI, Router
from ninja.security import django_auth
from ninja.security import HttpBearer
from django.http import HttpResponseForbidden
from django.http import HttpResponseForbidden, response
from http import HTTPStatus
from decouple import config 
from api.versions.v1.apis.index import router as indexrouter


from django.utils import timezone
# import jwt

# authenticator =  GlobalAuth() if config('ENVIRONMENT') == 'production' else None
api = NinjaAPI(
    title="Multi Tenacy School Management Api Interface",
    description="This is an API with dynamic OpenAPI info section.",
)


api.add_router("/", indexrouter)



