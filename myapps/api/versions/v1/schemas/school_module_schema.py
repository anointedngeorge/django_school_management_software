from ninja import Schema, Field, UploadedFile
from typing import Optional, List

import uuid
import pydantic


class ClassseOut(Schema):
    id:uuid.UUID = None
    name:str = None

class SectionNameOut(Schema):
    id:uuid.UUID = None
    name:str = None


class ClasssectionsOut(Schema):
    name: SectionNameOut = None
    classes:ClassseOut = None