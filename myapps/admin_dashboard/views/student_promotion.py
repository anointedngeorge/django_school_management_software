from typing import Any
from django.http.request import HttpRequest as HttpRequest
from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic import RedirectView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from coreattrs.user_permissions_context import UserPermissions
from django.contrib import messages as django_message

from myschool.forms.result_form import PrintResultForm
from ..forms import LoginForm
from typing import List
from coreattrs.error_messages import ErrorMessages
from admin_dashboard.views.functions import check_user, PAGE_NOT_FOUND, admin_custom_permission_required
from django.apps import apps
from urllib.parse import urlencode
# load business logic


BASE_DIR_NAME = "admin_custom"
APP_NAMESPACE = "admin_dashboard"
LOGIN_URL = f'/{BASE_DIR_NAME}/'
LOGIN_NAMESPACE = f"{APP_NAMESPACE}:login"
ON_SUCCESS_URL = f"{APP_NAMESPACE}:redirect_url"



class StudentPromotion(TemplateView): 
    template_name = f"{BASE_DIR_NAME}/promotions/student_promotion.html"

    @method_decorator(login_required(login_url=reverse_lazy(LOGIN_NAMESPACE)))
    @method_decorator(admin_custom_permission_required)
    def dispatch(self, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
 
        context['page_title'] = f"Student Promotion"
        # Add additional context data if needed
        return context
    
    def post(self, request, *args, **kwargs):
        try:
            from myschool.models import StudentPromotion, Students

            from_classes = request.POST.get('from_classes')
            from_sections = request.POST.get('from_sections')

            to_classes = request.POST.get('to_classes')
            to_sections = request.POST.get('to_sections')
            # 
            promotion_values = request.POST.getlist('promotion')

            student_promoted = StudentPromotion.objects.all()
            students_group =  Students.objects.all()
            
            
            for x in promotion_values:
                data = {
                        'student_id':int(x), 
                        'previous_classes_id':from_classes, 
                        'previous_sections_id':from_sections,
                        'current_classes_id':to_classes,
                        'current_sections_id':to_sections
                    }
                if student_promoted.filter(student_id=int(x)).exists():
                    objdata = student_promoted.update(
                        previous_classes_id=from_classes,
                        previous_sections_id=from_sections,
                        current_classes_id=to_classes,
                        current_sections_id=to_sections
                    )
                    if objdata:
                        students_group.update(classes_id=to_classes, sections_id=to_sections)
                        django_message.success(request, f"Promotion Created")
                        # return redirect(request.META.get("HTTP_REFERER"))
                else:
                    objdata = student_promoted.create(**data)
                    print(objdata)
                    if objdata:
                        students_group.update(classes_id=to_classes, sections_id=to_sections)
                        django_message.success(request, f"Promotion Created")
            return redirect(request.META.get("HTTP_REFERER"))
        except Exception as e:
            import traceback
            traceback.print_exc()
            return redirect(request.META.get("HTTP_REFERER"))

