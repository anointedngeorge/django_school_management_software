from django.contrib import admin
from decouple import config
from myschool.plugins.code_generator import shuffler


@admin.action(description='Reset Registration Code')
def resetRegistrationCode(self, request, queryset):
    try:
        for x in queryset:
            if x.code != "": 
                pass
            else:
                code = shuffler(w1=x.first_name, w2=x.last_name, size=8, step=1)
                x.code = code
                x.save()
        return queryset
    except:
        pass

