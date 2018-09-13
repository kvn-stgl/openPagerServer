from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView

from pager.forms import CustomAlarmCreateForm
from pager.models import Alarm, Device


class AlarmIndexView(LoginRequiredMixin, ListView):
    context_object_name = 'alarm_list'
    model = Alarm

    def get_queryset(self):
        """Return the last five published questions."""
        return super().get_queryset().filter(owner=self.request.user.id).order_by('-time')


class AlarmDetailView(LoginRequiredMixin, DetailView):
    model = Alarm

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user.id)

class AlarmCreateView(LoginRequiredMixin, CreateView):
    form_class = CustomAlarmCreateForm
    template_name = 'pager/alarm_create_form.html'

class AlarmDeleteView(DeleteView):
    model = Alarm
    success_url = reverse_lazy('alarm-list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user.id)

class DeviceIndexView(LoginRequiredMixin, ListView):
    context_object_name = 'device_list'
    model = Device

    def get_queryset(self):
        """Return the last five published questions."""
        return super().get_queryset().filter(owner=self.request.user.id)


class DeviceDetailView(LoginRequiredMixin, DetailView):
    model = Device

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user.id)


class DeviceDeleteView(DeleteView):
    model = Device
    success_url = reverse_lazy('device-list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user.id)


