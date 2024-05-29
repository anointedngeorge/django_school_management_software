from django.contrib import admin
from myschool.models.school_users import Students

@admin.register(Students)
class SchoolStudentsAdmin(admin.ModelAdmin):
    pass


