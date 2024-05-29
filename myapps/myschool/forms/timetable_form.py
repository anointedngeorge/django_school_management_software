from django import forms
# from django.contrib.postgres.forms.jsonb import JSONField
import json
from myschool.models.school_module import SubjectSelection
from myschool.models.school_users import Students
from myschool.models.result import Results
from myschool.models.attendance import Attendance
from django.forms.widgets import TextInput, TimeInput
import importlib
from datetime import datetime
import calendar

from myschool.models.timetable import Timetable


class TimetableForm(forms.ModelForm):

    class Meta:
        model=Timetable
        fields= ['time','subject','days']
        widgets = {
            'time': forms.TimeInput(attrs={'type':'time','class':'form form-control'}),
        }

