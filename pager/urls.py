from django.urls import path

from . import views

app_name = 'pager'

urlpatterns = [
    path('', views.AlarmIndexView.as_view(), name='alarms'),
    path('alarm/<int:pk>', views.AlarmDetailView.as_view(), name='alarm-detail'),
    path('alarm/<int:pk>/delete', views.AlarmDeleteView.as_view(), name='alarm-delete'),
    path('alarm/create', views.AlarmCreateView.as_view(), name='alarm-create'),

    path('devices', views.DeviceIndexView.as_view(), name='devices'),
    path('devices/<int:pk>', views.DeviceDetailView.as_view(), name='device-detail'),
    path('devices/<int:pk>/delete', views.DeviceDeleteView.as_view(), name='device-delete'),
]
