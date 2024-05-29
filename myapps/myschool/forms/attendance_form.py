from django import forms
# from django.contrib.postgres.forms.jsonb import JSONField
import json
from myschool.models.school_module import SubjectSelection
from myschool.models.school_users import Students
from myschool.models.result import Results
from myschool.models.attendance import Attendance
from django.forms.widgets import TextInput
import importlib
from datetime import datetime
import calendar

class AttendanceForm(forms.ModelForm):

    class Meta:
        model=Attendance
        fields= ['subject','teacher','classes','sections','term','session']





class AttendanceSheet(forms.Form):

    def __init__(self, context={}, *args, **kwargs):
        super(AttendanceSheet, self).__init__(*args, **kwargs)

