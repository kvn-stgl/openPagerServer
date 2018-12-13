import hashlib
import time

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser, UserManager
from django.db import models
from django.template import Template, Context, TemplateSyntaxError


class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
    objects = CustomUserManager()

    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True)

    def is_organization_admin(self):
        return self.organization.owner.id == self.id


class Organization(models.Model):
    owner = models.ForeignKey(get_user_model(), related_name='owner', on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, verbose_name="Adresse")
    plz = models.CharField(max_length=5, verbose_name="PLZ")
    place = models.CharField(max_length=100, verbose_name="Ort")

    access_key = models.CharField(max_length=64)

    # This will probably change in the future to the user roles
    push_title = models.CharField(max_length=255, verbose_name="Titel",
                                  default="{{ Keywords_EmergencyKeyword }} - {{ Keywords_Keyword }}")
    push_message = models.TextField(verbose_name="Nachricht",
                                    default=
                                    """Einsatz vom {{ Timestamp }} (Einsatzzeitpunkt)
Stichwörter: {{ Keywords }}
Hinweis: {{ Comment }}

Einsatzort: {{ Einsatzort }}
Fahrzeuge:
{{ Resources }}
""")

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


class OperationPropertyLocation(models.Model):
    location = models.CharField(max_length=200, verbose_name="Location", default="", blank=True, )
    zip_code = models.CharField(max_length=5, verbose_name="Postleitzahl", default="", blank=True, )
    city = models.CharField(max_length=200, verbose_name="Stadt", default="", blank=True, )
    street = models.CharField(max_length=200, verbose_name="Straße", default="", blank=True, )
    street_number = models.CharField(max_length=10, verbose_name="Straßennummer", default="", blank=True, )
    intersection = models.CharField(max_length=200, verbose_name="Kreuzung", default="", blank=True, )
    geo_latitude = models.DecimalField(verbose_name="Latitude", null=True, blank=True, max_digits=42, decimal_places=30)
    geo_longitude = models.DecimalField(verbose_name="Longitude", null=True, blank=True, max_digits=42,
                                        decimal_places=30)

    def __str__(self):
        parts = []
        if self.street:
            parts.append(self.street)
            if (self.street_number):
                parts.append(" " + self.street_number)
            parts.append(", ")

        if self.zip_code:
            parts.append(self.zip_code)

        if self.city:
            if self.zip_code:
                parts.append(" ")
            parts.append(self.city)

        return "".join(parts).strip()


class OperationKeywords(models.Model):
    keyword = models.CharField(max_length=10, verbose_name="Schlagwort", blank=True, default="")
    emergency_keyword = models.CharField(max_length=10, verbose_name="Stichwort", blank=True, default="")

    def __str__(self):
        parts = []
        if self.emergency_keyword:
            parts.append("Stichwort: " + self.emergency_keyword)

        if self.keyword:
            parts.append("Schlagwort: " + self.keyword)

        return ", ".join(parts)


class Operation(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    operation_guid = models.CharField(max_length=128, verbose_name="GUID")
    operation_number = models.CharField(max_length=20, verbose_name="Operation Nummer", default="", blank=True, )
    timestamp = models.DateTimeField(verbose_name="Alarmzeit")
    timestamp_income = models.DateTimeField(auto_now_add=True, verbose_name="Alarmeingang")
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

    @property
    def expression_dict(self):
        dict = {
            "Timestamp": self.timestamp,
            "Comment": self.comment,
        }
        if self.keywords:
            dict.update({
                "Keywords": str(self.keywords),
                "Keywords_EmergencyKeyword": self.keywords.emergency_keyword,
                "Keywords_Keyword": self.keywords.keyword,
            })

        if self.einsatzort:
            dict.update({
                "Einsatzort": str(self.einsatzort),
                "Einsatzort_City": self.einsatzort.city,
                "Einsatzort_Zip": self.einsatzort.zip_code,
                "Einsatzort_Street": self.einsatzort.street,
                "Einsatzort_StreetNumber": self.einsatzort.street_number,
                "Einsatzort_Intersection": self.einsatzort.intersection,
                "Einsatzort_Location": self.einsatzort.location,
                "Einsatzort_Longitude": self.einsatzort.geo_longitude,
                "Einsatzort_Latitude": self.einsatzort.geo_latitude,
            })

        if self.zielort:
            dict.update({
                "Zielort": str(self.zielort),
                "Zielort_City": self.zielort.city,
                "Zielort_Zip": self.zielort.zip_code,
                "Zielort_Street": self.zielort.street,
                "Zielort_StreetNumber": self.zielort.street_number,
                "Zielort_Intersection": self.zielort.intersection,
                "Zielort_Location": self.zielort.location,
                "Zielort_Longitude": self.zielort.geo_longitude,
                "Zielort_Latitude": self.zielort.geo_latitude
            })

        # resources = self.operationresource_set.all()
        # if resources:
        #     dict.update({"Resources": resources})

        return dict

    @property
    def push_title_formatted(self):
        try:
            t = Template(self.organization.push_title)
            c = Context(self.expression_dict)
            return t.render(c)
        except TemplateSyntaxError as err:
            return err

    @property
    def push_message_formatted(self):
        try:
            t = Template(self.organization.push_message)
            c = Context(self.expression_dict)
            return t.render(c)
        except TemplateSyntaxError as err:
            return err

    def __str__(self):
        return '{} ({})'.format(self.operation_guid, self.keywords)

    class Meta:
        ordering = ['-timestamp']


class OperationResource(models.Model):
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=200, verbose_name="Name")
    timestamp = models.CharField(max_length=200, verbose_name="Timestamp", default="", blank=True, )

    def __str__(self):
        return '{} (um {})'.format(self.full_name, self.timestamp)


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
