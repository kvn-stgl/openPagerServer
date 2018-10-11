from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from pager.models import Alarm, Device, CustomUser, Organization

"""Integrate with admin module."""

from django.contrib import admin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'organization', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'organization')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'organization')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ['name']

    list_display = ('name', 'address', 'owner')
    list_filter = ('name', 'owner')


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
    list_filter = ('device', 'manufacturer', 'platform')
