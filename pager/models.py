from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models


class Alarm(models.Model):

    owner = models.ForeignKey(get_user_model(), related_name='owner', on_delete=models.CASCADE)
    receivers = models.ManyToManyField(get_user_model(), related_name='receivers')

    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    message = models.TextField
    destination = models.CharField(max_length=100, null=True)
    destination_lat = models.CharField(max_length=15, null=True)
    destination_lng = models.CharField(max_length=15, null=True)


class Device(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    fcm_token = models.CharField(max_length=32)

    # Stuff from Xamarin.DeviceInfo
    device = models.CharField(max_length=20, null=True)
    manufacturer = models.CharField(max_length=20, null=True)
    device_name = models.CharField(max_length=20, null=True)
    version = models.CharField(max_length=10, null=True)
    platform = models.CharField(max_length=10, null=True)
    idiom = models.CharField(max_length=10, null=True)
