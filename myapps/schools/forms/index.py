from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from schools.models import Schools

class SchoolForm(forms.ModelForm):

    class Meta:
        model=Schools
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for x in self.fields:
            self.fields[x].widget.attrs.update({'class': 'form-control'})

