from django.contrib import admin
from decouple import config

@admin.action(description='Activate Courses')
def activate_courses(self, request, queryset):
    print(queryset)
    return 


@admin.action(description='Url Switcher')
def change_url(self, request, queryset):
    BASE_APP_NAME =  config("BASE_APP_NAME")
    for x in queryset:
        # split url with /, and filter out empty string ('')
        splited =  [e for e in str(x.url).split("/") if e != '']
        if len(splited) > 1:
            splited[0] = BASE_APP_NAME
            st = "/".join(splited)
            x.url = f"/{st}/"
            x.save()
    return queryset