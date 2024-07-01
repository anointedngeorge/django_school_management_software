from django.db import models
from django.db.models import Q
from django.urls import reverse
from myschool.plugins.session_generator import sessionGenerator
from myschool.core_attrs import CoreAttrs
from django.utils import timezone
from myschool.core import CoreBaseModel
from myschool.plugins.generate_filename import generate_filename
from django.utils.html import format_html
from myschool.plugins.code_generator import actionparam
from django.template.loader import render_to_string
import requests
import re


BASE_ADMIN_DIR = 'admin_custom'
BASE_ADMIN_URI = 'admin_dashboard'

class Subjects(CoreBaseModel, CoreAttrs):
    name = models.CharField(max_length=150, blank=True, null=True)
    desc = models.CharField(max_length=150, blank=True, null=True, verbose_name='description')

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self) -> str:
        return f"{self.name}"
    
    def list_display(self):
        return ['name','desc']
    
    # def form(self):
    #     from myschool.forms.myforms import SubjectsForm
    #     return SubjectsForm

    def  save(self, *args, **kwargs):
        # convert the names to upper case
        complex_filter = Q(name=str(self.name).title()) | Q(name=str(self.name).upper()) | Q(name=str(self.name).lower())
        m = self._meta.model.objects.filter(complex_filter)
        if m.exists():
            pass
        else:
            self.name = str(self.name).title()
            super().save(*args, **kwargs)


class SectionsNames(CoreBaseModel, CoreAttrs):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'Section Name'
        verbose_name_plural = 'Section Names'

    def __str__(self) -> str:
        return f"Section: {self.name}"
    
    def list_display(self):
        return ['id','name']
    
    # def form(self):
    #     from myschool.forms.myforms import SectionNamesForm
    #     return SectionNamesForm
    
    def save(self, *args, **kwargs):
        # convert the names to upper case
        m = self._meta.model.objects.filter(name=str(self.name).upper())
        if m.exists():
            pass
        else:
            self.name = str(self.name).upper()
            super().save(*args, **kwargs)




class Sections(CoreBaseModel, CoreAttrs):
    name = models.ForeignKey("myschool.SectionsNames", on_delete=models.CASCADE, null=True, related_name="section_names_rel")
    classes =  models.ForeignKey("myschool.Classes", on_delete=models.CASCADE, null=True)
    desc = models.CharField(max_length=150, blank=True, null=True, verbose_name='description')

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'
        ordering=('id',)
        
    def __str__(self) -> str:
        return f"{self.classes} - {self.name}"
    

    def list_display(self):
        return ['name','classes','desc']
    # def form(self):
    #     from myschool.forms.myforms import SectionsForm
    #     return SectionsForm
    
    def save(self, *args, **kwargs):
        
        complex_filter = Q(name_id=str(self.name.id)) & Q(classes_id=str(self.classes_id))
        
        m = self._meta.model.objects.filter(complex_filter)
        print(m.exists())
        if m.exists():
            pass
        else:
            super().save(*args, **kwargs)


class Classes(CoreBaseModel, CoreAttrs):
    name = models.CharField(max_length=150, blank=True, null=True)
    desc = models.CharField(max_length=150, blank=True, null=True, verbose_name='description')

    class Meta:
        verbose_name = 'Classes'
        verbose_name_plural = 'Classes'
        ordering=('-id',)
        
    def __str__(self) -> str:
        return f"{self.name}"
    
    def list_display(self):
        return ['name','desc']

    
    def  save(self, *args, **kwargs):
        # convert the names to upper case
        complex_filter = Q(name=str(self.name).title()) | Q(name=str(self.name).upper()) | Q(name=str(self.name).lower())
        m = self._meta.model.objects.filter(complex_filter)
        if m.exists():
            pass
        else:
            self.name = str(self.name).title()
            super().save(*args, **kwargs)


class Term(CoreBaseModel, CoreAttrs):
    name = models.CharField(max_length=150, blank=True, null=True)
    desc = models.CharField(max_length=150, blank=True, null=True, verbose_name='description')

    class Meta:
        verbose_name = 'Term'
        verbose_name_plural = 'Terms'
        
    def __str__(self) -> str:
        return f"{self.name}"
    def list_display(self):
        return ['name','desc']
    # def form(self):
    #     from myschool.forms.myforms import SessionForm
    #     return SessionForm
    
    def  save(self, *args, **kwargs):
        # convert the names to upper case
        complex_filter = Q(name=str(self.name).title()) | Q(name=str(self.name).upper()) | Q(name=str(self.name).lower())
        m = self._meta.model.objects.filter(complex_filter)
        if m.exists():
            pass
        else:
            self.name = str(self.name).title()
            super().save(*args, **kwargs)
    


class SubjectSelection(CoreBaseModel, CoreAttrs):
    subject =  models.ForeignKey("myschool.Subjects", on_delete=models.CASCADE, null=True, related_name="rel_subject_selected")
    teacher = models.ForeignKey("myschool.Teachers", on_delete=models.CASCADE, related_name="rel_teacher_selected")
    classes = models.ForeignKey("myschool.Classes", on_delete=models.CASCADE, related_name="rel_classes_selected")
    sections = models.ForeignKey("myschool.Sections", on_delete=models.CASCADE, related_name="rel_sections_selected")
    session = models.CharField(max_length=250, choices=sessionGenerator(), null=True)
    term = models.ForeignKey("myschool.Term", on_delete=models.CASCADE, related_name="rel_term_selected")

    class Meta:
        verbose_name = 'Teacher Subject'
        verbose_name_plural = 'Teacher Subjects'
        ordering=('-id',)
        
    def __str__(self) -> str:
        return f"{self.teacher} {self.subject} {self.session}"

    def extra(self):
        query = {"teacher_id":self.teacher.id,
                 "sections_id":self.sections.id,
                 "classes_id":self.classes.id,
                 "term_id":self.term.id,
                 "subject_id":self.subject.id,
                 "session":self.session
                }
        add_url =  reverse(f"{BASE_ADMIN_URI}:addnewresults", kwargs=query)
        change_url =  reverse(f"{BASE_ADMIN_URI}:editnewresults", kwargs=query)
        
    
        context = {"dropdown_menus":[
            actionparam(classicon='fa fa-card-0', has_modal=False, 
                        is_active=True, 
                        title="Add Result",
                        url=f"{add_url}",
                        query={}
                    ),
                    actionparam(classicon='fa fa-card-0', has_modal=False, 
                        is_active=True, 
                        title="Edit Result",
                        url=f"{change_url}",
                        query={}
                    )
        ]}
        template_name = f"{BASE_ADMIN_DIR}/dropdown/menu1.html"
        return render_to_string(template_name=template_name, context=context)

    
    def list_display(self):
        return ['extra','subject','teacher','classes','sections','term','session']
    
    # def form(self):
    #     from myschool.forms.myforms import SubjectSelectionForm
    #     return SubjectSelectionForm
    
    def save(self, *args, **kwargs):
        complex_filter = (
                          Q(subject_id=str(self.subject.id)) 
                          & Q(classes_id=str(self.classes_id))
                          & Q(sections_id=str(self.sections.id))
                          & Q(term_id=str(self.term.id))
                          & Q(teacher_id=str(self.teacher.id))
                          & Q(session=str(self.session))
                        )
        m = self._meta.model.objects.filter(complex_filter)
        if m.exists():
            pass
        else:
            super().save(*args, **kwargs)
    



# Student Promotion section
class StudentPromotion(CoreBaseModel, CoreAttrs):
    student =  models.OneToOneField("myschool.Students", on_delete=models.CASCADE, related_name='student_promotion')
    
    previous_classes = models.ForeignKey("myschool.Classes", on_delete=models.CASCADE, related_name="rel_previous_classes_promotion")
    previous_sections = models.ForeignKey("myschool.Sections", on_delete=models.CASCADE, related_name="rel_previous_sections_promotion")

    current_classes = models.ForeignKey("myschool.Classes", on_delete=models.CASCADE, related_name="rel_classes_promotion")
    current_sections = models.ForeignKey("myschool.Sections", on_delete=models.CASCADE, related_name="rel_sections_promotion")
    
    promotion_time = models.TimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'Student Promotion'
        verbose_name_plural = 'Student Promotions'
        ordering=('-id',)
        
    def __str__(self) -> str:
        return f"{self.student}"
    
    def undo(self):
        return "Button"

    def list_display(cls):
        return ['student','previous_classes','previous_sections','current_classes','current_sections','created','promotion_time','undo']