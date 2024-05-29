from django.shortcuts import render
from django.views.defaults import page_not_found



def handler_404(request, exception):
    return render(
            request=request, 
            status=404,
            template_name="admin/404.html",
        )

