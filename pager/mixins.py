from django.contrib.auth.mixins import AccessMixin

from pager.models import Organization


class OrganizationIdRequiredMixin(AccessMixin):
    """Verify that the current user is in the correct organization."""
    kwargs_argument = "pk"

    def get_organization_id(self, **kwargs):
        return kwargs[self.kwargs_argument]

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.organization_id != self.get_organization_id(**kwargs):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class HasOrganizationRequiredMixin(AccessMixin):
    """Verify that the current user is in the correct organization."""
    kwargs_argument = "pk"

    def get_organization_id(self, **kwargs):
        return kwargs[self.kwargs_argument]

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.organization_id:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class OrganizationAdminRequiredMixin(AccessMixin):
    """Verify that the current user is admin of the organization."""

    def dispatch(self, request, *args, **kwargs):
        if not Organization.objects.get(pk=request.user.organization_id).owner == request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
