from django.db  import models



class UserPermissions(models.TextChoices):
    ADMIN = 'admin','Admin'
    STAFF = 'staff','Staff'
