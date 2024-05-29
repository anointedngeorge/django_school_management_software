from django.contrib import admin
from django.http.response import HttpResponse
from authuser.models import *
import uuid
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from authuser.forms import *

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # search_fields = ["email__startswith"]
    list_display = ["id", "email", "username", "code", "is_staff", "is_superuser"]
    list_filter = ["is_superuser"]
    list_display_links = ["email", "username"]
    # filter_horizontal = []
    ordering = ["id"]
    exclude = ["last_login", "groups", "user_permissions"]
    form = UserRegistrationForm

    # def response_add(self, request, obj, post_url_continue=None) -> HttpResponse:
    #     coded = str(uuid.uuid4()).replace("-", "")[:8]
    #     code = f"{coded}"
    #     obj.code = code
    #     obj.save()
    #     return super().response_add(request, obj, post_url_continue)


