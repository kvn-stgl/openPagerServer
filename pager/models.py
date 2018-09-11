from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractUser

class Alarm(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    message = models.TextField
    destination = models.CharField(max_length=100, null=True)
    destination_lat = models.CharField(max_length=15, null=True)
    destination_lng = models.CharField(max_length=15, null=True)


class Device(models.Model):
    DEVICE_CHOICES = (
        ('I', 'iOS'),
        ('A', 'Android'),
        ('U', 'Unknown')
    )

    mail = models.CharField(max_length=32)
    fcm_token = models.CharField(max_length=32)
    os = models.CharField(max_length=1, choices=DEVICE_CHOICES, default='U')

    # Stuff from Xamarin.DeviceInfo
    device = models.CharField(max_length=60, null=True)
    manufacturer = models.CharField(max_length=60, null=True)
    device_name = models.CharField(max_length=60, null=True)
    version = models.CharField(max_length=60, null=True)
    platform = models.CharField(max_length=60, null=True)
    idiom = models.CharField(max_length=60, null=True)
