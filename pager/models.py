import hashlib
import time
from enum import Enum

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import PermissionsMixin, AbstractUser, UserManager
from django.db import models
from django.conf import settings


class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
    objects = CustomUserManager()


class Organization(models.Model):
    owner = models.ForeignKey(get_user_model(), related_name='owner', on_delete=models.CASCADE)
    members = models.ManyToManyField(get_user_model(), through='Membership', related_name='members')

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, verbose_name="Adresse")
    plz = models.CharField(max_length=5, verbose_name="PLZ")
    place = models.CharField(max_length=100, verbose_name="Ort")

    access_key = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        if not self.pk:

            m = hashlib.sha256()
            m.update(self.name.encode())
            m.update(settings.SECRET_KEY.encode())
            m.update(str(time.time()).encode())

            self.access_key = m.hexdigest()
        super(Organization, self).save(*args, **kwargs)

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
    title = models.CharField(max_length=200, verbose_name="Titel")
    keyword = models.CharField(max_length=100, null=True, blank=True, verbose_name="Stichwort")

    message = models.TextField(verbose_name="Beschreibung")

    destination = models.CharField(max_length=100, null=True, blank=True, verbose_name="Einsatzadresse")
    destination_lat = models.CharField(max_length=15, null=True, blank=True, verbose_name="Latitude")
    destination_lng = models.CharField(max_length=15, null=True, blank=True, verbose_name="Longitude")

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
