from django.db import models
from .core_attrs import CoreAttrs
import uuid
from django.utils import timezone


class CoreBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created=  models.DateField(auto_created=True, default=timezone.now, editable=False)
    
    
    class Meta:
        abstract = True