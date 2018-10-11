from django.db.models.signals import post_save
from django.dispatch import receiver

from pager.models import Alarm, Device
from pager.sender.python_fcm import PythonFcm


@receiver(post_save, sender=Alarm)
def send_alarm(sender, instance: Alarm, created, **kwargs):
    if created:
        devices = Device.objects.filter(owner_id__in=instance.organization.customuser_set.all())

        sender = PythonFcm(devices)

        # delete all devices with invalid recipients
        error_tokens, debug = sender.send(instance)
        if error_tokens:
            Device.objects.filter(fcm_token__in=error_tokens).delete()

        instance.debug_response = debug
        instance.save()
