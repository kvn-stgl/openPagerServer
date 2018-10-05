from django.db.models import Count
from django.http import Http404
from rest_auth.views import LoginView
from rest_framework import viewsets, permissions, mixins
from rest_framework.authentication import TokenAuthentication

from api.permissions import IsOwner
from api.serializers import AlarmSerializer, DeviceSerializer, OrganizationSerializer
from pager.models import Alarm, Device, Organization


class LoginViewCustom(LoginView):
    authentication_classes = (TokenAuthentication,)


# Create your views here.
class AlarmViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Alarm.objects.order_by('-time')
    serializer_class = AlarmSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_fields = ('organization',)

    # schema = CustomSchema()

    def get_queryset(self):
        return super().get_queryset() \
            .filter(organization__membership__user=self.request.user) \
            .prefetch_related('organization')

    def create(self, request, *args, **kwargs):
        """
        input:
          - name: access_key
            type: string
            required: true
            location:
        """
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        token = serializer.validated_data['access_key']

        organization = Organization.objects.filter(access_key=token).first()
        if organization:
            serializer.save(organization=organization)
        else:
            raise Http404("Organization not found")


class DeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset() \
            .annotate(num=Count('name')) \
            .filter(membership__user=self.request.user) \
            .order_by('owner')
