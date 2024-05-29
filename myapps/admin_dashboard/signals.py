import math
import os
from django.conf import settings
from django.db.models.signals import post_save,pre_save
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from decouple import config

# from coreattrs.admin_permissions_context import UserPermissions
from admin_dashboard.plugins.code_generator import shuffler
from django.utils import timezone



def to_html(template:str, context:dict):
    from django.template.loader import render_to_string
    from django.conf import settings
    from django.utils import timezone
    try:
        d = os.path.abspath(f"email_template/{template}")
        html_message = render_to_string(template_name=f"email_template/{template}", context=context)
        return html_message
    except Exception as e:
        return f"{e}"


