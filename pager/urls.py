from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from . import views

router = routers.DefaultRouter()
router.register(r'alarms', views.AlarmViewSet)
router.register(r'devices', views.DeviceViewSet)

schema_view = get_swagger_view(title='OpenPager API')

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/swagger', schema_view),
    url(r'^api/v1/auth/', include('rest_framework.urls', namespace='rest_framework'))
]