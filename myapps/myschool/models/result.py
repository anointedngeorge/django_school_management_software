from django.db import models
from myschool.plugins.session_generator import sessionGenerator

from myschool.core_attrs import CoreAttrs
import uuid
from django.utils import timezone
from myschool.core import CoreBaseModel
from myschool.plugins.generate_filename import generate_filename
from django.utils.html import format_html
import importlib


# print(sessionGenerator())
class Results(CoreBaseModel, CoreAttrs):
    teacher =  models.ForeignKey("myschool.Teachers", on_delete=models.CASCADE)
    classes =  models.ForeignKey("myschool.Classes", on_delete=models.CASCADE)
    sections =  models.ForeignKey("myschool.Sections", on_delete=models.CASCADE)
    term =  models.ForeignKey("myschool.Term", on_delete=models.CASCADE)
    subject =  models.ForeignKey("myschool.Subjects", on_delete=models.CASCADE)
    session = models.CharField(max_length=250, choices=sessionGenerator(), null=True)
    result = models.JSONField(default=list)

    def __str__(self) -> str:
        return f"{self.teacher}-{self.term}"

    class Meta:
        verbose_name = 'Result'
        verbose_name_plural = 'Results'

    def list_display(self):
        return ['teacher','sections','classes','term','subject','session']
    
    def list_filter(self):
        return ['term','session']

    # def form(self):
    #     from myschool.forms.result_form import ResultForm
    #     return ResultForm
    
    def extra_forms(self):
        try:
            from myschool.forms.result_form import EditResultStudentForm
            return {'form':EditResultStudentForm}
        except:
            return dict