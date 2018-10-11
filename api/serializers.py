import rest_auth.serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers

from pager.models import Alarm, Device, Organization

# Get the UserModel
UserModel = get_user_model()


class LoginSerializer(rest_auth.serializers.LoginSerializer):
    def get_fields(self):
        fields = super(LoginSerializer, self).get_fields()
        del fields['username']
        return fields

    def validate(self, attrs):
        return super(LoginSerializer, self).validate(attrs)


class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        exclude = ('organization', 'debug_response')


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        exclude = ('owner',)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        exclude = ('access_key', 'owner')
