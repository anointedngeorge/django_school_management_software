from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.http import HttpResponse
from django.db.models.query_utils import Q
from django.contrib.auth.forms import UserCreationForm
from authuser.models import *
from django.forms.fields import MultipleChoiceField,CharField


class UserRegistrationForm(UserCreationForm):
    # email = forms.EmailField(required=True)
    class Meta:
        model = CustomUser
        fields = "__all__"
        exclude = [
            "last_login",
            "groups",
            "user_permissions",
            "is_activeCustomUserverified",
            "token_pin_id",
            "token",
            "key",
            "message",
            "encoded",
            "encrypt_date",
            "rsa_duration",
            "is_token_verified",
            "is_online",
            # "password"
        ]

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2


