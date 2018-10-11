import hashlib
import time

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
    objects = CustomUserManager()

    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True)


class Organization(models.Model):
    owner = models.ForeignKey(get_user_model(), related_name='owner', on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, verbose_name="Adresse")
    plz = models.CharField(max_length=5, verbose_name="PLZ")
    place = models.CharField(max_length=100, verbose_name="Ort")

    access_key = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        if not self.pk:
            access_key = hashlib.sha256()
            access_key.update(self.name.encode())
            access_key.update(settings.SECRET_KEY.encode())
            access_key.update(str(time.time()).encode())

            self.access_key = access_key.hexdigest()
        super(Organization, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)


class Alarm(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, verbose_name="Titel")
    keyword = models.CharField(max_length=100, null=True, blank=True, verbose_name="Stichwort")

    message = models.TextField(verbose_name="Beschreibung")

    destination = models.CharField(max_length=100, null=True, blank=True, verbose_name="Einsatzadresse")
    destination_lat = models.CharField(max_length=15, null=True, blank=True, verbose_name="Latitude")
    destination_lng = models.CharField(max_length=15, null=True, blank=True, verbose_name="Longitude")

    debug_response = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{} ({})'.format(self.title, self.time)

    class Meta:
        ordering = ['-time']


class Device(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    fcm_token = models.CharField(max_length=200, primary_key=True)

    # Stuff from Xamarin.DeviceInfo
    device = models.CharField(max_length=20, null=True)
    manufacturer = models.CharField(max_length=20, null=True)
    device_name = models.CharField(max_length=20, null=True)
    version = models.CharField(max_length=10, null=True)
    platform = models.CharField(max_length=10, null=True)

    def __str__(self):
        return '{}'.format(self.device_name)
