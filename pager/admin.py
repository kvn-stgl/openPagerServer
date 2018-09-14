from django.contrib.auth.admin import UserAdmin

from pager.models import Alarm, Device, CustomUser

"""Integrate with admin module."""

from django.contrib import admin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser


@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    ordering = ['-time']
    search_fields = ['title', 'organization']

    list_display = ('title', 'time', 'organization')
    list_filter = ('organization',)
    date_hierarchy = 'time'

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    search_fields = ['device_name', 'owner']

    list_display = ('device_name', 'device', 'owner')
    list_filter = ('device','manufacturer','platform')