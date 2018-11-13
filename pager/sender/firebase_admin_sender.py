from typing import List

from firebase_admin import messaging
from firebase_admin.messaging import ApiCallError

from pager.firebase import firebase_app
from pager.models import Device, Operation


class FirebaseAdminSender:
    def __init__(self, devices: List[Device]):
        self.devices = devices

    def send(self, operation: Operation):
        message = messaging.Message(
            notification=messaging.Notification(
                title=operation.keywords,
                body=operation.keywords,
            )
        )

        error_tokens = []

        for device in self.devices:
            message.token = device.fcm_token

            try:
                messaging.send(message, app=firebase_app, dry_run=False)
            except ApiCallError as err:
                code = err.code

                # Old error list
                # error_list = ['MissingRegistration', 'MismatchSenderId', 'InvalidRegistration', 'NotRegistered']

                error_list = ['invalid-registration-token',
                              'registration-token-not-registered',
                              'invalid-package-name',
                              'invalid-recipient',
                              'invalid-argument']
                if code in error_list:
                    error_tokens.append(device.fcm_token)

        return error_tokens
