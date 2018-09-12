from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from rest_framework import viewsets

from pager.models import Alarm, Device
from pager.permissions import IsOwner
from .serializers import AlarmSerializer, DeviceSerializer


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

class AlarmIndexView(LoginRequiredMixin, ListView):
    template_name = 'pager/alarm/index.html'
    context_object_name = 'alarm_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Alarm.objects.order_by('-time')

class DeviceIndexView(LoginRequiredMixin, ListView):
    template_name = 'pager/device/index.html'
    context_object_name = 'device_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Device.objects.all()