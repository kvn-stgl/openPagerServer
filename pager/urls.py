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

    path('organization/operations', views.OperationIndexView.as_view(), name='operation-list'),
    path('operation/<int:pk>', views.OperationDetailView.as_view(), name='operation-detail'),
    path('operation/<int:pk>/delete', views.OperationDeleteView.as_view(), name='operation-delete'),
    path('organization/operation/create', views.operationCreate, name='operation-create'),
    path('organization/<int:pk>/operation/resend', views.operationResend, name='operation-resend'),

    path('devices', views.DeviceIndexView.as_view(), name='device-list'),
    path('devices/<str:pk>', views.DeviceDetailView.as_view(), name='device-detail'),
    path('devices/<str:pk>/delete', views.DeviceDeleteView.as_view(), name='device-delete'),
]
