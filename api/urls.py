from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from api import views

router = routers.DefaultRouter()
router.register(r'alarms', views.AlarmViewSet)
router.register(r'devices', views.DeviceViewSet)

schema_view = get_swagger_view(title='OpenPager API')

app_name = 'api'

urlpatterns = [
    url(r'^v1/', include(router.urls)),
    url(r'^v1/swagger', schema_view),
    url(r'^v1/auth/', include('rest_framework.urls', namespace='rest_framework')),
]
