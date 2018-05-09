from django.contrib.auth.models import User, Group
from rest_framework import serializers

from pager.models import Alarm, Device


class AlarmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alarm
        fields = '__all__'

class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'