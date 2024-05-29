from django.contrib import admin
from django.contrib.auth.models import Group

# Unregister the Group model from the admin site
admin.site.unregister(Group)