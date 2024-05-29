from ninja import Schema, Field, UploadedFile
from typing import Optional, List
import uuid
import pydantic


class MoneySerializer(Schema):
    amount: float = None
    code:str = None