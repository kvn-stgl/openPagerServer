from django.db.models.signals import post_save
from django.dispatch import receiver

from pager.models import Device, Operation
from pager.sender.python_fcm import PythonFcm


@receiver(post_save, sender=Operation)
def send_alarm(sender, instance: Operation, created, **kwargs):
    if created:
        devices = Device.objects.filter(owner_id__in=instance.organization.customuser_set.all())

        send_engine = PythonFcm(devices)

        # delete all devices with invalid recipients
        error_tokens, debug = send_engine.send(instance)
        if error_tokens:
            Device.objects.filter(fcm_token__in=error_tokens).delete()

        instance.debug_response = debug
        instance.save()
