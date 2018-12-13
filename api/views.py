from rest_auth.views import LoginView, LogoutView
from rest_framework import viewsets, permissions, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.permissions import IsOwner
from api.put_as_create import AllowPUTAsCreateMixin
from api.serializers import DeviceSerializer, OrganizationSerializer, OperationSerializer
from pager.models import Device, Organization, Operation


class LoginViewCustom(LoginView):
    authentication_classes = (TokenAuthentication,)


class LogoutViewCustom(LogoutView):
    authentication_classes = (TokenAuthentication,)


# Create your views here.
class OperationViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Operation.objects
    serializer_class = OperationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return super().get_queryset() \
            .filter(organization=self.request.user.organization) \
            .prefetch_related('organization')

    def perform_create(self, serializer):
        token = serializer.validated_data.pop('access_key')

        organization = Organization.objects.filter(access_key=token).first()
        if organization:
            serializer.save(organization=organization)
        else:
            raise PermissionDenied("AccessKey not valid")


class DeviceViewSet(AllowPUTAsCreateMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def perform_create(self, serializer, **kwargs):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class OrganizationDetail(mixins.ListModelMixin, GenericViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = super().get_queryset().get(pk=self.request.user.organization.id)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
