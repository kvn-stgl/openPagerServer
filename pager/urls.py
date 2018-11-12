from django.urls import path

from . import views

app_name = 'pager'

urlpatterns = [

    path('', views.OrganizationIndexView.as_view(), name='organization-list'),
    path('organization/create', views.OrganizationCreateView.as_view(),
         name='organization-create'),
    path('organization/<int:pk>', views.OrganizationDetailView.as_view(), name='organization-detail'),
    path('organization/<int:pk>/leave', views.MembershipLeaveView.as_view(), name='membership-leave'),
    path('organization/<int:pk>/delete', views.OrganizationDeleteView.as_view(), name='organization-delete'),

    path('membership/add', views.membershipAdd, name='membership-add'),
    path('membership/<int:pk>/delete', views.MembershipDeleteView.as_view(), name='membership-delete'),

    path('organization/alarms', views.AlarmIndexView.as_view(), name='alarm-list'),
    path('alarm/<int:pk>', views.AlarmDetailView.as_view(), name='alarm-detail'),
    path('alarm/<int:pk>/delete', views.AlarmDeleteView.as_view(), name='alarm-delete'),
    path('organization/alarm/create', views.alarmCreate, name='alarm-create'),
    path('organization/<int:pk>/alarm/resend', views.alarmResend, name='alarm-resend'),

    path('devices', views.DeviceIndexView.as_view(), name='device-list'),
    path('devices/<str:pk>', views.DeviceDetailView.as_view(), name='device-detail'),
    path('devices/<str:pk>/delete', views.DeviceDeleteView.as_view(), name='device-delete'),
]
