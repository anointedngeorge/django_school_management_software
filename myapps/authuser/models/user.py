from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from authuser.important_choices import *
# from geoposition.fields import GeopositionField
# from django.contrib.gis.db import models as gModels

from authuser.core_attrs import CoreAttrs
from user_permissions_context import UserPermissions
import uuid


class CustomUserManager(BaseUserManager):
    def _create_user(self, username, password, email, **extra_fields):
        if not email:
            raise ValueError("You have not provided a vaild email address")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(username, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(("email address"), unique=True, null=True)
    password = models.CharField(max_length=200)
    username = models.CharField(max_length=200, null=True, blank=True, unique=True)
    code = models.CharField(
        max_length=300, editable=False,null=True, blank=True,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_online = models.BooleanField(
        default=False, help_text="Checks online status."
    )
    
    permissions = models.CharField(max_length=150, choices=UserPermissions.choices, blank=True, null=True)
    
    finger_signature = models.CharField(max_length=350, null=True, blank=True)

    created = models.DateField(auto_now=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Authusers"
        verbose_name_plural = "Authusers"

    def __str__(self):
        return self.email

    def get_username(self):
        return self.username

    # def get_full_name(self):
    #     return f"{self.email} - {self.username}"

    # def get_short_name(self):
    #     return self.email.split('@')[0]
    
    # def natural_key(self):
    #     return self.email.split("@")[0]
    
    

