import math
import os
from django.conf import settings
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from decouple import config
from myschool.models.attendance import Attendance
from user_permissions_context import UserPermissions
from myschool.plugins.code_generator import shuffler


from myschool.models.school_users import Students,Teachers,Parents


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



@receiver(post_save, sender=Students)
def student_signals(sender, instance, created, **kwargs):
    try:
        if created:
            # create a code and also a permission
            shuf = shuffler(w1=instance.first_name, w2=instance.last_name, size=8)
            students =  instance.students
            students.permissions = UserPermissions.STUDENT
            students.code = shuf
            students.save()
    except Exception as e:
        return f"{e}"


@receiver(post_save, sender=Teachers)
def teachers_signals(sender, instance, created, **kwargs):
    try:
        if created:
            shuf = shuffler(w1=instance.first_name,w2=instance.last_name,size=8)
            instance.permissions = UserPermissions.TEACHER
            instance.code = shuf
            instance.save()
    except Exception as e:
        return f"{e}"


@receiver(post_save, sender=Parents)
def parents_signals(sender, instance, created, **kwargs):
    try:
        if created:
            shuf = shuffler(w1=instance.first_name,w2=instance.last_name,size=8)
            instance.permissions = UserPermissions.PARENT
            instance.code = shuf
            instance.save()
    except Exception as e:
        return f"{e}"




@receiver(post_save, sender=Attendance)
def register_attendence_signals(sender, instance, created, **kwargs):
    try:
        if created:
            shuf = shuffler(w1="register",w2="attendance",size=15)
            instance.code = shuf
            instance.save()
    except Exception as e:
        return f"{e}"