from ninja import Router, Form, File, UploadedFile
from typing import List, Optional, Dict, Union
from django.template.loader import render_to_string
from datetime import datetime
from typing import List

from api.versions.v1.message.status_message import StatusMessage


router = Router(tags=["Index API"])


@router.get("/")
def index(request):
    return {'message':'welcome to index page'}