from django.conf.urls import url
from django.urls import include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from api import views
from api.views import LoginViewCustom, LogoutViewCustom

router = routers.DefaultRouter()
router.register(r'alarms', views.AlarmViewSet)
router.register(r'devices', views.DeviceViewSet)
router.register(r'organizations', views.OrganizationViewSet)

schema_view = get_swagger_view(title='OpenPager API')

app_name = 'api'

urlpatterns = [
    url(r'^v1/', include(router.urls)),
    url(r'^v1/swagger', schema_view),
    url(r'^v1/auth/login/$', LoginViewCustom.as_view(), name='rest_login'),
    url(r'^v1/auth/logout/$', LogoutViewCustom.as_view(), name='rest_logout'),
    url(r'^v1/auth/', include('rest_framework.urls', namespace='rest_framework')),
]
