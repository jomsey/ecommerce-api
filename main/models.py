from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name='email address',unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=150 ,blank=True)
    
    class Meta(AbstractUser.Meta):
           swappable = 'AUTH_USER_MODEL'


