from ninja import Router, Form, File, UploadedFile
from typing import List, Optional, Dict, Union
from django.template.loader import render_to_string
from datetime import datetime
from typing import List

from api.versions.v1.message.status_message import StatusMessage
from myschool.models.school_module import *
from myschool.models.school_users import *
from pathlib import Path
from api.versions.v1.schemas.school_module_schema import *
import os


BASE_DIR = Path(__file__).resolve().parent.parent

VERSION = 'V1'

router = Router(tags=["School Utilities"])


@router.get("/loadhtmlclasssections/{class_id}/", response={200:StatusMessage, 401:StatusMessage, 500:StatusMessage})
def get_html_classe_sections(request, class_id:str):
    try:
        context = {}
        queryset = Sections.objects.all().filter(classes_id=class_id).order_by('-id')
        if queryset.exists():
            context['sections'] = queryset
            filename = f"admin_custom/api_pages/sections.html"
            template = render_to_string(request=request, template_name=filename, context=context)
            return 200, StatusMessage(message=template)
        else:
            return 401, StatusMessage(message="Empty")
    except Exception as e:
        return 500, StatusMessage(message=str(e))
    

@router.get("/loadhtmlstudents/{class_id}/{section_id}/", response={200:StatusMessage, 401:StatusMessage, 500:StatusMessage})
def get_html_students(request, class_id:str, section_id:str):
    try:
        context = {}
        queryset = Students.objects.all().filter(classes_id=class_id, sections_id=section_id).order_by('-id')
        if queryset.exists():
            context['students'] = queryset
            filename = f"admin_custom/api_pages/student_select.html"
            template = render_to_string(request=request, template_name=filename, context=context)
            return 200, StatusMessage(message=template)
        else:
            return 401, StatusMessage(message="Empty")
    except Exception as e:
        return 500, StatusMessage(message=str(e))