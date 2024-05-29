from django.conf import settings
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
# from matrixpro.submodel.m_client import ClientClass
from decouple import config
from authuser.models import *
import os


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


