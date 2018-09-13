import rest_auth.serializers

from django.contrib.auth import get_user_model
from rest_framework import serializers

from pager.models import Alarm, Device

# Get the UserModel
UserModel = get_user_model()

class LoginSerializer(rest_auth.serializers.LoginSerializer):
    def get_fields(self):
        fields = super(LoginSerializer, self).get_fields()
        del fields['username']
        return fields

    def validate(self, attrs):
        return super(LoginSerializer, self).validate(attrs)

class AlarmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alarm
        fields = ('id', 'time', 'title', 'destination', 'destination_lat', 'destination_lng')


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'fcm_token', 'os', 'manufacturer', 'device_name', 'version', 'platform', 'idiom')
