
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.contrib import messages as msg
from decouple import config

import zipfile
import re
import os
from ..admin import loadModuleAttribute
from ..models import Plugins, SystemSettings
# Plugins = loadModuleAttribute(f"{config('APP_MAIN_NAME')}.models", 'Plugins')
redirect_path = f"/{config('BASE_APP_NAME')}"


def settings(request, context=None):
    try:
        from ..forms.settings_form import SettingsForm
        import json
        settingform = SettingsForm()
        context['form'] = settingform
        if request.POST:
            path = config("SETTINGS_JSON_PATH")
            # print(path)
            dt = request.POST.dict()
            dt.pop("csrfmiddlewaretoken")
            # dp = json.dumps(dt)
            if os.path.exists(path):
                dat = SystemSettings.objects.all()
                if dat.exists():
                    dat.filter(id=1).update(
                        settings=dt
                    )
                else:
                    dat.create(
                        settings=dt
                    )
                # print(d)
            else:
                print("No")
            
        return TemplateResponse(
            request=request,
            template="admin/settings/settings.html",
            context=context,
            status=200,
        )
    except Exception as e:
        # print(e, 'error!')
        return str(e)


def plugins(request, context=None):
    try:
        pl = Plugins.objects.all()
        if request.method == 'POST' and 'file' in request.FILES:
            uploaded_file = request.FILES['file']

            if request.POST.get('plugin_type') != "":
                with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                    file_names = zip_ref.namelist()
                    ft = str(zip_ref.filename).rsplit(".")
                    # word = word_to_underscore(ft[0]).lower()
                
                    f = f"{ft[0]}/plugins.html"

                    if f in file_names:
                        pt = f"templates/admin/plugins"
                        # pt = f"{config('APP_MAIN_NAME')}/templates/admin/plugins"
                        # create this plugin's directory if it does not exist.
                        if not os.path.exists(os.path.realpath(pt)):
                            os.makedirs(pt)
                        template_file = f"admin/plugins"
                        listdir = os.listdir(pt)
                        if not ft[0] in listdir:
                            zip_ref.extract(f'{ft[0]}/plugins.html', path=pt)
                         
                            pl.create(
                                name=ft[0],
                                file_path=f"{pt}/{ft[0]}/plugins.html",
                                status = False,
                                plugin_type=request.POST.get("plugin_type"),
                                directory=f"{pt}/{ft[0]}",
                                template_file=f"{template_file}/{ft[0]}/plugins.html",
                            )
                            msg.success(request=request, message="Plugin Upload Successful!")
                        else:
                            msg.warning(request=request, message=f"Plugin already exists!")
                    else:
                        msg.warning(request=request, message=f"These {f} files must be present.")
            else:
                msg.warning(request, "Fields must not be empty")
        # printout the plugin
        context['plugins'] = pl
        return TemplateResponse(
            request=request,
            template="admin/settings/plugins.html",
            context=context,
            status=200,
        )
    except Exception as e:
        return HttpResponse('An error occurred: {}'.format(e))


