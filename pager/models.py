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


class OperationPropertyLocation(models.Model):
    location = models.CharField(max_length=200, verbose_name="Location", default="", blank=True, )
    zip_code = models.CharField(max_length=5, verbose_name="Postleitzahl", default="", blank=True, )
    city = models.CharField(max_length=200, verbose_name="Stadt", default="", blank=True, )
    street = models.CharField(max_length=200, verbose_name="Straße", default="", blank=True, )
    street_number = models.CharField(max_length=10, verbose_name="Straßennummer", default="", blank=True, )
    intersection = models.CharField(max_length=200, verbose_name="Kreuzung", default="", blank=True, )
    geo_latitude = models.DecimalField(verbose_name="Latitude", null=True, max_digits=15, decimal_places=12)
    geo_longitude = models.DecimalField(verbose_name="Longitude", null=True, max_digits=15, decimal_places=12)

    def __str__(self):
        return '{} ({} {}, {})'.format(self.location, self.street, self.street_number, self.city)


class OperationKeywords(models.Model):
    keyword = models.CharField(max_length=10, verbose_name="Stichwort")
    emergency_keyword = models.CharField(max_length=10, verbose_name="Schlagwort")

    def __str__(self):
        return '{} ({})'.format(self.keyword, self.emergency_keyword)


class Operation(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    guid = models.CharField(max_length=128, verbose_name="GUID")
    operation_number = models.CharField(max_length=20, verbose_name="Operation Nummer", default="", blank=True, )
    alarm_at = models.DateTimeField(verbose_name="Alarmzeit")
    income_at = models.DateTimeField(auto_now_add=True, verbose_name="Alarmeingang")
    messenger = models.CharField(max_length=200, verbose_name="Mitteiler", default="", blank=True, )
    comment = models.TextField(verbose_name="Kommentar", default="", blank=True, )
    plan = models.CharField(max_length=200, verbose_name="Plan", default="", blank=True, )
    priority = models.CharField(max_length=100, verbose_name="Priorität", default="", blank=True, )

    debug_response = models.TextField(null=True, blank=True)

    einsatzort = models.OneToOneField(
        OperationPropertyLocation,
        on_delete=models.CASCADE,
        null=True,
        related_name="einsatzort"
    )

    zielort = models.OneToOneField(
        OperationPropertyLocation,
        on_delete=models.CASCADE,
        null=True,
        related_name="zielort"
    )

    keywords = models.OneToOneField(
        OperationKeywords,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return '{} ({})'.format(self.guid, self.keywords)

    class Meta:
        ordering = ['-income_at']


class OperationResource(models.Model):
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=200, verbose_name="Name")
    timestamp = models.CharField(max_length=200, verbose_name="Timestamp", default="", blank=True, )

    def __str__(self):
        return '{} ({})'.format(self.full_name, self.timestamp)


class OperationLoop(models.Model):
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    loop = models.CharField(max_length=10, verbose_name="Schleife", )


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
