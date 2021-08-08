from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Usermodel(AbstractUser) :
    class Meta :
        db_table = "my_user"

#    username = models.CharField(max_length=20, null = False)
#    password = models.CharField(max_length=256, null = False)
    bio = models.TextField(max_length=500, blank=True)
#    created_at = models.DateTimeField(auto_now_add=True)
#    updated_at = models.DateTimeField(auto_now=True)
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name= 'followee')