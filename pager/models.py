from enum import Enum

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import PermissionsMixin, AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
    objects = CustomUserManager()


class Organization(models.Model):
    owner = models.ForeignKey(get_user_model(), related_name='owner', on_delete=models.CASCADE)
    members = models.ManyToManyField(get_user_model(), through='Membership', related_name='members')

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.name)

class Membership(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_member = models.BooleanField(null=False, default=False)

    class Meta:
        unique_together = (('user', 'organization'),)


class Alarm(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    message = models.TextField(null=False, blank=True)
    destination = models.CharField(max_length=100, null=True)
    destination_lat = models.CharField(max_length=15, null=True)
    destination_lng = models.CharField(max_length=15, null=True)

    def __str__(self):
        return '{} ({})'.format(self.title, self.time)


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

    def __str__(self):
        return '{}'.format(self.device_name)
