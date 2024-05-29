from django.db  import models



class UserPermissions(models.TextChoices):
    ADMIN = 'admin','Admin'
    STUDENT = 'student','Student'
    TEACHER = 'teacher','Teacher'
    PARENT = 'parent','Parent'
    ACCOUNTANT = 'accountant','Accountant'