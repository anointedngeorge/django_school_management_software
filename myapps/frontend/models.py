from django.db import models
from myschool.plugins.session_generator import sessionGenerator
from myschool.core_attrs import CoreAttrs
import uuid
from django.utils import timezone
from myschool.core import CoreBaseModel
from myschool.plugins.generate_filename import generate_filename
from django.utils.html import format_html


# Create your models here.

class Sliders(CoreBaseModel, CoreAttrs):
    title = models.CharField(max_length=150, null=True, blank=True)
    desc = models.CharField(max_length=300, null=True, blank=True)
    is_allowed = models.BooleanField(default=False, choices=[(False,'Never'),(True,'Show')])
    img = models.ForeignKey("gentelella.Media", on_delete=models.SET_NULL, null=True)
    index = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = 'Slider'
        verbose_name_plural = 'Sliders'

    def _img(self):
        if not self.img:
            img = f"<img src='...' alt='...' width=50 height=50 />"
            return format_html(img)
        else:
            img = f"<img src='{self.img.file.url}' width=50 height=50 />"
            return format_html(img)

    def list_display(self):
        return ['_img','title','desc','is_allowed','index']


class Aboutus(CoreBaseModel, CoreAttrs):
    title = models.CharField(max_length=150, null=True, blank=True)
    seo_title = models.CharField(max_length=150, null=True, blank=True)
    seo_description = models.CharField(max_length=350, null=True, blank=True)

    content =  models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = 'About'
        verbose_name_plural = 'About us'

    def save(self, *args, **kwargs) -> None:
        id = uuid.UUID("350ae9e2-094d-44e4-8d24-1abf8dda7bbe")
        self._meta.model.objects.filter(id=id).delete()
        self.pk = id
        super().save(*args, **kwargs)
        
    def list_display(self):
        return ['title','seo_title','seo_description']
