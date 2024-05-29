from django import forms
# from django.contrib.postgres.forms.jsonb import JSONField
import json
from myschool.models.school_module import *
from myschool.models.school_users import *

from django.forms.widgets import TextInput
import importlib
from datetime import datetime
import calendar

EXCLUDED_FIELDS = [
            'last_login',
            'groups',
            'date_joined',
            'photo',
            'is_superuser',
            'is_active',
            'is_staff'
        ]

class StudentsForm(forms.ModelForm):

    class Meta:
        model=Students
        fields= ['first_name','middle_name','last_name','username', 'email','phone','password','classes', 'sections', 'user_permissions']
        exclude = EXCLUDED_FIELDS
      
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for x in self.fields:
            name = self.fields[x].label
            self.fields[x].widget.attrs.update({'class': 'form-control', 'placeholder':str(name)})



class TeachersForm(forms.ModelForm):

    class Meta:
        model=Teachers
        fields= ['first_name','middle_name','last_name','username', 'email','phone','password','user_permissions']
        exclude = EXCLUDED_FIELDS
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for x in self.fields:
            name = self.fields[x].label
            self.fields[x].widget.attrs.update({'class': 'form-control', 'placeholder':str(name)})





class ClassesForm(forms.ModelForm):

    class Meta:
        model=Classes
        fields= "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for x in self.fields:
            name = self.fields[x].label
            self.fields[x].widget.attrs.update({'class': 'form-control', 'placeholder':str(name)})

class SessionForm(forms.ModelForm):

    class Meta:
        model=Term
        fields= "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for x in self.fields:
            name = self.fields[x].label
            self.fields[x].widget.attrs.update({'class': 'form-control', 'placeholder':str(name)})

class SectionsForm(forms.ModelForm):

    class Meta:
        model=Sections
        fields= "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for x in self.fields:
            name = self.fields[x].label
            self.fields[x].widget.attrs.update({'class': 'form-control', 'placeholder':str(name)})


class SubjectsForm(forms.ModelForm):

    class Meta:
        model=Subjects
        fields= "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for x in self.fields:
            name = self.fields[x].label
            self.fields[x].widget.attrs.update({'class': 'form-control', 'placeholder':str(name)})


class SectionNamesForm(forms.ModelForm):

    class Meta:
        model=SectionsNames
        fields= "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for x in self.fields:
            name = self.fields[x].label
            self.fields[x].widget.attrs.update({'class': 'form-control', 'placeholder':str(name)})

class SubjectSelectionForm(forms.ModelForm):

    class Meta:
        model=SubjectSelection
        fields= "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for x in self.fields:
            name = self.fields[x].label
            self.fields[x].widget.attrs.update({'class': 'form-control', 'placeholder':str(name)})

