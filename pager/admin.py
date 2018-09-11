from pager.models import Alarm, Device

"""Integrate with admin module."""

from django.contrib import admin


@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    pass

@admin.register(Device)
class AlarmAdmin(admin.ModelAdmin):
    pass