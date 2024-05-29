from typing import Union
from pydantic import BaseModel
from ninja import Router


class StatusMessage(BaseModel):
    message:str