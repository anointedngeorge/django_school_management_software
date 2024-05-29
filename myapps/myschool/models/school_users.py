from typing import Iterable
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User as CustomUser
# from authuser.models import CustomUser
from myschool.actions.myschool_actions import resetRegistrationCode
from myschool.plugins.generate_filename import generate_filename
from myschool.core_attrs import  CoreAttrs
from myschool.core import CoreBaseModel
from django.utils.html import format_html
import uuid


USERS_EXCLUDED =  [
            "last_login",
            "groups",
            "user_permissions",
            'is_active',
            'is_online',
            'permissions',
            'is_staff',
            'is_superuser',
            'finger_signature'
        ]


class Students(CustomUser, CoreAttrs):
    code = models.CharField(max_length=150, blank=True, null=True)
    permissions = models.CharField(max_length=150, blank=True, null=True)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=150, blank=True, null=True)
    parent_registration_code = models.CharField(max_length=150, blank=True, null=True)
    # parent_phone = models.CharField(max_length=150, blank=True, null=True)
    # parent_email = models.CharField(max_length=150, blank=True, null=True)
    # parent_address = models.CharField(max_length=150, blank=True, null=True)
    sections = models.ForeignKey("myschool.Sections", on_delete=models.CASCADE, related_name='student_sections')
    classes = models.ForeignKey("myschool.Classes", on_delete=models.CASCADE, related_name='student_classes')
    photo = models.ImageField(upload_to=generate_filename)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def get_username(self) -> str:
        return f"{self.first_name}"

    def profile(self):
        if not self.photo:
            img = f"<img src='...' alt='...' width=50 height=50 />"
            return format_html(img)
        else:
            img = f"<img src='{self.photo.url}' width=50 height=50 />"
            return format_html(img)
    def extra(self):
        from myschool.plugins.code_generator import actionparam
        from django.template.loader import render_to_string
        import requests
        context = {"dropdown_menus":[
            actionparam(classicon='fa fa-card-0', has_modal=False, 
                        is_active=True, title="Print ID",
                        url=f"/console/myschool/students/view/printidcard/?=user_id={self.pk}"
                    )
        ]}
        template_name = "admin/dropdown/menu1.html"
        return render_to_string(template_name=template_name, context=context)
        
    def list_display(self):
        return ['code','profile','first_name','middle_name','last_name','email','sections','classes','permissions']
    
    def list_filter(self):
        return ['classes']
    
    @classmethod
    def exclude(cls):
        return USERS_EXCLUDED
    
    def action(self):
        return [resetRegistrationCode,"delete_selected"]
    # def form(self):
    #     from ..forms.myforms import StudentsForm
    #     return StudentsForm
    
    # def save(self, *args, **kwargs):
    #     complex_filter = Q(email=str(self.email))
    #     m = self._meta.model.objects.filter(complex_filter)
    #     if m.exists():
    #         pass
    #     else:
    #         super().save(*args, **kwargs)
    


class Teachers(CustomUser, CoreAttrs):
    code = models.CharField(max_length=150, blank=True, null=True)
    permissions = models.CharField(max_length=150, blank=True, null=True)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=150, blank=True, null=True)
    photo = models.ImageField(upload_to=generate_filename)

    show_on_frontend =  models.BooleanField(
                    default=False,
                    choices=[(True,"Yes"), (False,"No")]
                )

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def profile(self):
        if not self.photo:
            img = f"<img src='...' alt='...' width=50 height=50 />"
            return format_html(img)
        else:
            img = f"<img src='{self.photo.url}' width=50 height=50 />"
            return format_html(img)
        
    def extra(self):
        from myschool.plugins.code_generator import actionparam
        from django.template.loader import render_to_string
        import requests
        context = {"dropdown_menus":[
            actionparam(classicon='fa fa-file', has_modal=True, 
                        is_active=True, title="Register Subject",
                        url="/console/myschool/subjectselection/",
                        query={}
                    )
        ]}
        template_name = "admin/dropdown/menu1.html"
        return render_to_string(template_name=template_name, context=context)

    def list_display(self):
        return ['profile','first_name','middle_name','email','last_name','phone','extra']
    
    def list_display_links(self):
        return ['first_name','last_name']
    
    @classmethod
    def exclude(cls):
        return USERS_EXCLUDED
    # def form(self):
    #     from myschool.forms.myforms import TeachersForm
    #     return TeachersForm
    

class Parents(CustomUser, CoreAttrs):
    code = models.CharField(max_length=150, blank=True, null=True)
    permissions = models.CharField(max_length=150, blank=True, null=True)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'


    def list_display(self):
        return ['first_name','middle_name','last_name','phone']
    
    @classmethod
    def exclude(cls):
        return USERS_EXCLUDED
    
    def list_filter(self):
        return ['first_name']
    