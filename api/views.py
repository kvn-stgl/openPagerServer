from rest_framework import viewsets

from api.permissions import IsOwner
from api.serializers import AlarmSerializer, DeviceSerializer
from pager.models import Alarm, Device


# Create your views here.
class AlarmViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Alarm.objects.order_by('-time')
    serializer_class = AlarmSerializer
    #permission_classes = (permissions.IsAuthenticated,)


class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsOwner,)
