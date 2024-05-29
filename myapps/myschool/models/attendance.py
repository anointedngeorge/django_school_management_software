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


class Attendance(CoreBaseModel, CoreAttrs):
    subject =  models.ForeignKey("myschool.Subjects", on_delete=models.CASCADE, null=True, related_name="attendance_rel_subject_selected")
    teacher = models.ForeignKey("myschool.Teachers", on_delete=models.CASCADE, related_name="attendance_rel_teacher_selected")
    classes = models.ForeignKey("myschool.Classes", on_delete=models.CASCADE, related_name="attendance_rel_classes_selected")
    sections = models.ForeignKey("myschool.Sections", on_delete=models.CASCADE, related_name="attendance_rel_sections_selected")
    session = models.CharField(max_length=250, choices=sessionGenerator(), null=True)
    term = models.ForeignKey("myschool.Term", on_delete=models.CASCADE, related_name="attendance_rel_term_selected")
    code = models.CharField(max_length=150, null=True, editable=True)

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
    
    def __str__(self) -> str:
        return f"{self.subject} {self.teacher} {self.classes}"

    def list_display(self):
        return ['code','subject','teacher','classes','sections','session','term','extra']

    def list_display_links(self):
        return ['subject','teacher']
    

    def extra(self):
        url = f"{network('selected_student_attendance')}?code={self.code}"
        table = f"<a href='{url}' class='btn btn-sm btn-dark'><i class='fa fa-eye'></i></a>"
        return format_html(table)
    

class AttendanceRecords(CoreBaseModel, CoreAttrs):
    attendance_code = models.CharField(max_length=150,null=True, editable=False)
    attendance = models.ForeignKey("myschool.Attendance", on_delete=models.CASCADE, null=True, related_name="attendance_rel")
    student =  models.ForeignKey("myschool.Students", on_delete=models.CASCADE, null=True, related_name="attendance_rel_recorder")
    morning = models.CharField(max_length=150, null=True, blank=True, choices=[
        ('absent',"Absent"),
        ('present','Present')
    ])
    afternoon = models.CharField(max_length=150, null=True, blank=True, choices=[
        ('absent',"Absent"),
        ('present','Present')
    ])
    month_name = models.CharField(max_length=250, null=True, blank=True, choices=calenday_months())
    day_name = models.CharField(max_length=250, null=True, blank=True, choices=calenday_days())
    attendance_date = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = 'Student Record'
        verbose_name_plural = 'Student Records'

    def __str__(self) -> str:
        return f"{self.student}"
    
    def list_display(self):
        return ['attendance','student','morning','afternoon',
                'month_name','day_name','attendance_date']
    def list_filter(self):
        return ['attendance_date']