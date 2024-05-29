import uuid

from django.urls import reverse


def link(app='admin_dashboard',name='changelist', **kwargs):
    try:
        concat = f"{app}:{name}"
        url = reverse(concat, kwargs=kwargs)
        return url
    except Exception as e:
        return str(e)


DASHBOARD_CONTENTS = [
    
]


