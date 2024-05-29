
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.views.static import serve
from django.urls import path, include, re_path
from decouple import config
import importlib
import traceback
from .views import *    


app_name = "admin_dashboard"
urlpatterns = []
try:
    urlpatterns += [
        path(f"", LoginFunc.as_view(), name="login"),
        # path(f"redirect/user", RedirectAuthenticatedUser.as_view(), name="redirect_url"),  
        path(f"dashboard/", Dashboard.as_view(), name="dashboard"),
        path(f"profile/", ProfileFunc.as_view(), name="profile"),
        path(f"message/", MessageFunc.as_view(), name="message"),
     #    settings
        path(f"dashboard/settings/<str:name>", SettingsFun.as_view(), name="settings"),
     #    login redirect
        path(f"dashboard/redirect/authenticated/user", RedirectAuthenticatedUser.as_view(), name="redirect_url"),
     #    logout
        path(f"logout/", logoutFunc, name="logout"),

        # change list and change form parameter
        path(f"dashboard/<str:appname>/<str:modelname>/list", ChangeListFunc.as_view(), name="changelist"),
        path(f"dashboard/<str:appname>/<str:modelname>/create", ChangeFormFunc.as_view(), name="changeform"),
        path(f"dashboard/<str:appname>/<str:objectid>/<str:modelname>/change", UpdateFormFunc.as_view(), name="updateform"),
        path(f"dashboard/<str:appname>/<str:objectid>/<str:modelname>/delete", DeleteChangeListObject, name="delete"),
        path(f"dashboard/<str:appname>/<str:modelname>/modal", ModalChangeFormFunc.as_view(), name="modalchangeform"),
    
        # results
        path(f"dashboard/<str:subject_id>/<str:classes_id>/<str:sections_id>/<str:teacher_id>/<str:term_id>/<str:session>/add", 
             AddNewResult.as_view(), name="addnewresults"),
        path(f"dashboard/completeresult", completeResultUpload, name="completeresult"),
        path(f"dashboard/updateuploadedresult", updateUploadResult, name="updateuploadedresult"),
        
        path(f"dashboard/result-printing/", 
             PrintResults.as_view(), name="resultprinting"),

        path(f"dashboard/student/promotion", 
             StudentPromotion.as_view(), name="studentpromotion"),

        path(f"dashboard/<str:subject_id>/<str:classes_id>/<str:sections_id>/<str:teacher_id>/<str:term_id>/<str:session>/change", 
             EditNewResult.as_view(), name="editnewresults"),
    ]
except Exception as e:
    urlpatterns += []

