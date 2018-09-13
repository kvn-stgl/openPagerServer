from pager.models import Alarm, Device

"""Integrate with admin module."""

from django.contrib import admin


@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    ordering = ['-time']
    search_fields = ['title', 'owner']

    list_display = ('title', 'time', 'owner')
    list_filter = ('owner',)
    date_hierarchy = 'time'

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    search_fields = ['device_name', 'owner']

    list_display = ('device_name', 'device', 'owner')
    list_filter = ('device','manufacturer','platform')