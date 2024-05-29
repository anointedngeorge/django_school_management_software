from django.db import models
from myschool.plugins.system_calendar import calenday_days, calenday_months
from myschool.plugins.url import network
from myschool.plugins.session_generator import sessionGenerator

from myschool.core_attrs import CoreAttrs
import uuid
from django.utils import timezone
from myschool.core import CoreBaseModel
from myschool.plugins.generate_filename import generate_filename
from django.utils.html import format_html
import importlib


class Timetable(CoreBaseModel, CoreAttrs):
    time = models.TimeField(auto_now=False, null=True)
    subject =  models.ForeignKey("myschool.Subjects", on_delete=models.CASCADE, null=True, related_name="timetable_subject_rel")
    days = models.CharField(max_length=250, null=True, blank=True, choices=calenday_days())
   
    class Meta:
        verbose_name = 'TimeTable'
        verbose_name_plural = 'TimeTable'
    
    def __str__(self) -> str:
        return f"{self.subject} {self.days}"

    def list_display(self):
        return ['time','days','subject']

    def list_filter(self):
        return ['days']
    
    # def form(self):
    #     try:
    #         from myschool.forms.timetable_form import TimetableForm
    #         return TimetableForm
    #     except:
    #         pass
 