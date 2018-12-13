from django.conf.urls import url
from django.urls import include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from api import views
from api.views import LoginViewCustom, LogoutViewCustom

router = routers.DefaultRouter()
router.register(r'operations', views.OperationViewSet)
router.register(r'devices', views.DeviceViewSet)
router.register(r'organization', views.OrganizationDetail)

schema_view = get_swagger_view(title='OpenPager API')

app_name = 'api'

urlpatterns = [
    url(r'^v1/', include(router.urls)),
    url(r'^v1/swagger', schema_view),
    url(r'^auth/login/$', LoginViewCustom.as_view(), name='rest_login'),
    url(r'^auth/logout/$', LogoutViewCustom.as_view(), name='rest_logout'),
    url(r'^auth/', include('rest_auth.urls')),
]
