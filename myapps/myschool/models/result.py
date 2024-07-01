from django.db import models
from myschool.plugins.session_generator import sessionGenerator
from django.contrib.auth.models import User
from myschool.core_attrs import CoreAttrs
import uuid
from django.urls import reverse
from django.utils import timezone
from myschool.core import CoreBaseModel
from myschool.plugins.generate_filename import generate_filename
from django.utils.html import format_html
import importlib


class Results(CoreBaseModel, CoreAttrs):
    teacher =  models.ForeignKey("myschool.Teachers", on_delete=models.CASCADE)
    classes =  models.ForeignKey("myschool.Classes", on_delete=models.CASCADE)
    sections =  models.ForeignKey("myschool.Sections", on_delete=models.CASCADE)
    term =  models.ForeignKey("myschool.Term", on_delete=models.CASCADE)
    subject =  models.ForeignKey("myschool.Subjects", on_delete=models.CASCADE)
    session = models.CharField(max_length=250, choices=sessionGenerator(), null=True)
    result = models.JSONField(default=list, editable=False)

    def __str__(self) -> str:
        return f"{self.teacher}-{self.term}"

    class Meta:
        verbose_name = 'Result'
        verbose_name_plural = 'Results'
    
    def _view_result(self):
        
        return format_html('<a href="{}">View</a>', reverse('admin_dashboard:resultprinting', args=[]))


    def list_display(self):
        return ['teacher','sections','classes','term','subject','session','_view_result','result']
    
    def list_filter(self):
        return ['term','session']
    



class ResultComment(CoreBaseModel, CoreAttrs):
  
    classes =  models.ForeignKey("myschool.Classes", on_delete=models.CASCADE)
    sections =  models.ForeignKey("myschool.Sections", on_delete=models.CASCADE)
    term =  models.ForeignKey("myschool.Term", on_delete=models.CASCADE)
    subject =  models.ForeignKey("myschool.Subjects", on_delete=models.CASCADE)
    session = models.CharField(max_length=250, choices=sessionGenerator(), null=True)
    comment = models.JSONField(null=True)
    
   
    def __str__(self) -> str:
        return f"{self.subject}-{self.term}"

    class Meta:
        verbose_name = 'Result Comments'
        verbose_name_plural = 'Result Comment'
    

    def list_display(self):
        return ['classes','sections','subject', 'term','session']
    
    def list_filter(self):
        return ['term','session']

