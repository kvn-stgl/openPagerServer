from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions

from pager.models import Alarm, Device
from pager.permissions import IsOwner
from .serializers import AlarmSerializer, DeviceSerializer


class AlarmViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer
    #permission_classes = (permissions.IsAuthenticated,)


class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsOwner,)
