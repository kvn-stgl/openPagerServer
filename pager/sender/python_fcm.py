from datetime import timezone
from typing import List

from pyfcm import FCMNotification

from openPagerServer import settings
from pager.models import Device, Operation


class PythonFcm:
    def __init__(self, devices: List[Device]):
        self.devices = devices
        self.push_service = FCMNotification(api_key=settings.FCM_API_KEY)

    def send(self, operation: Operation):
        registration_ids = [device.fcm_token for device in self.devices]

        # Sending a notification with data message payload
        data_message = {
            "type": "operation",
            "key": operation.operation_guid,
            "title": operation.keywords,
            "message": operation.keywords,
            "destination": operation.einsatzort,
            "destination_lat": operation.einsatzort.geo_longitude,
            "destination_lng": operation.einsatzort.geo_latitude,
            "time": int(operation.timestamp.replace(tzinfo=timezone.utc).timestamp())
        }

        # To multiple devices
        result = self.push_service.notify_multiple_devices(registration_ids=registration_ids, data_message=data_message)

        return self._list_with_error_results(
            registration_ids,
            result['results']
        ), str(result)

    def _list_with_error_results(self, registration_ids, results):
        error_tokens = []
        for (index, item) in enumerate(results):
            if 'error' in item:
                error_list = ['MissingRegistration', 'MismatchSenderId', 'InvalidRegistration', 'NotRegistered']
                if item['error'] in error_list:
                    registration_id = registration_ids[index]
                    error_tokens.append(registration_id)
        return error_tokens
