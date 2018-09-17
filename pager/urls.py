from django.urls import path, reverse

from . import views

app_name = 'pager'

urlpatterns = [

    path('', views.OrganizationIndexView.as_view(), name='organization-list'),
    path('organization/create', views.OrganizationCreateView.as_view(),
         name='organization-create'),
    path('organization/<int:pk>', views.OrganizationDetailView.as_view(), name='organization-detail'),
    path('organization/<int:pk>/leave', views.MembershipLeaveView.as_view(), name='membership-leave'),
    path('organization/<int:pk>/delete', views.OrganizationDeleteView.as_view(), name='organization-delete'),

    path('membership/<int:pk>/add', views.membershipAdd, name='membership-add'),
    path('membership/<int:pk>/delete', views.MembershipDeleteView.as_view(), name='membership-delete'),

    path('alarms/<int:pk>', views.AlarmIndexView.as_view(), name='alarm-list'),
    path('alarm/<int:pk>', views.AlarmDetailView.as_view(), name='alarm-detail'),
    path('alarm/<int:pk>/delete', views.AlarmDeleteView.as_view(), name='alarm-delete'),
    path('alarm/create', views.AlarmCreateView.as_view(), name='alarm-create'),

    path('devices', views.DeviceIndexView.as_view(), name='device-list'),
    path('devices/<int:pk>', views.DeviceDetailView.as_view(), name='device-detail'),
    path('devices/<int:pk>/delete', views.DeviceDeleteView.as_view(), name='device-delete'),
]
