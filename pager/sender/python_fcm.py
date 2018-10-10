import uuid
from datetime import timezone
from typing import List

from pyfcm import FCMNotification

from openPagerServer import settings
from pager.models import Device, Alarm


class PythonFcm:
    def __init__(self, devices: List[Device]):
        self.devices = devices
        self.push_service = FCMNotification(api_key=settings.FCM_API_KEY)

    def send(self, alarm: Alarm):
        registration_ids = [device.fcm_token for device in self.devices]

        # Sending a notification with data message payload
        data_message = {
            "type": "operation",
            "key": str(uuid.uuid4()),
            "title": alarm.title,
            "message": alarm.message,
            "destination": alarm.destination,
            "destination_lat": alarm.destination_lat,
            "destination_lng": alarm.destination_lng,
            "time": int(alarm.time.replace(tzinfo=timezone.utc).timestamp())
        }

        # To multiple devices
        result = self.push_service.notify_multiple_devices(registration_ids=registration_ids, data_message=data_message)

        return self._list_with_error_results(
            registration_ids,
            result['results']
        )

    def _list_with_error_results(self, registration_ids, results):
        error_tokens = []
        for (index, item) in enumerate(results):
            if 'error' in item:
                error_list = ['MissingRegistration', 'MismatchSenderId', 'InvalidRegistration', 'NotRegistered']
                if item['error'] in error_list:
                    registration_id = registration_ids[index]
                    error_tokens.append(registration_id)
        return error_tokens
