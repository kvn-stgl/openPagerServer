from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectTemplateResponseMixin

from openPagerServer import settings
from pager.forms import CustomOrganizationCreateForm, MembershipAddForm, OperationCreateForm, OperationKeywordForm, \
    OperationPropertyLocationForm, PushMessageForm
from pager.mixins import OrganizationIdRequiredMixin, HasOrganizationRequiredMixin, OrganizationAdminRequiredMixin
from pager.models import Device, Organization, Operation
from pager.signals import send_alarm


class OrganizationIndexView(LoginRequiredMixin, SingleObjectTemplateResponseMixin, View):
    template_name = "pager/organization_index.html"

    def get(self, request, *args, **kwargs):
        if request.user.organization:
            return redirect('pager:organization-detail', pk=request.user.organization.id)

        context = {}
        context.update(**kwargs)
        return self.render_to_response(context)


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    form_class = CustomOrganizationCreateForm
    template_name = 'pager/organization_create_form.html'
    success_url = reverse_lazy('pager:organization-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class OrganizationSettingsPushView(OrganizationAdminRequiredMixin, UpdateView):
    form_class = PushMessageForm
    template_name = 'pager/organization_settings_push_form.html'
    success_url = reverse_lazy('pager:organization-settings-push')

    def get_object(self, queryset=None):
        return Organization.objects.get(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Push-Einstellungen geändert.')
        return super().form_valid(form)


class OrganizationDeleteView(OrganizationAdminRequiredMixin, DeleteView):
    model = Organization
    success_url = reverse_lazy('pager:organization-list')

    def get_object(self, queryset=None):
        return Organization.objects.get(owner=self.request.user)


class OrganizationDetailView(OrganizationIdRequiredMixin, DetailView):
    model = Organization
    form_class = MembershipAddForm


@login_required
def membershipAdd(request):
    organization = request.user.organization

    if organization.owner_id != request.user.id:
        raise PermissionDenied('No permission to add user.')

    if request.method == "POST":
        form = MembershipAddForm(organization, request.POST)
        if form.is_valid():
            new_user = form.cleaned_data['user']
            new_user.organization = organization
            new_user.save()
            return redirect('pager:organization-detail', pk=organization.id)
    else:
        form = MembershipAddForm(organization)

    return render(request, 'pager/membership_add_form.html', {'form': form, 'organization': organization})


class MembershipLeaveView(OrganizationIdRequiredMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy('pager:organization-list')
    template_name_suffix = '_confirm_leave_from_organization'

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.organization = None
        self.object.save()

        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse_lazy('pager:organization-list')


class MembershipDeleteView(DeleteView):
    model = get_user_model()
    template_name_suffix = '_confirm_delete_from_organization'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.organization = None
        self.object.save()

        return HttpResponseRedirect(success_url)

    def get_queryset(self):
        return super().get_queryset().filter(organization__owner=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy('pager:organization-detail', kwargs={'pk': self.get_object().organization.id})


class OperationIndexView(HasOrganizationRequiredMixin, ListView):
    context_object_name = 'operation_list'
    model = Operation

    def get_queryset(self):
        return self.request.user.organization.operation_set.all()


class OperationDetailView(HasOrganizationRequiredMixin, DetailView):
    model = Operation

    def get_queryset(self):
        return super().get_queryset().filter(organization=self.request.user.organization)


@login_required
def operationCreate(request):
    organization = request.user.organization

    if organization.owner != request.user:
        raise Http404('No matches the given query.')

    if request.method == "POST":
        form_op = OperationCreateForm(organization, request.POST)
        form_keyword = OperationKeywordForm(request.POST)
        form_einsatzort = OperationPropertyLocationForm(request.POST)
        if form_op.is_valid() and form_keyword.is_valid():
            keywords = form_keyword.save()
            einsatzort = form_einsatzort.save()

            alarm = form_op.save(commit=False)
            alarm.keywords = keywords
            alarm.einsatzort = einsatzort
            alarm.save()

            return redirect('pager:operation-detail', pk=alarm.id)
    else:
        form_op = OperationCreateForm(organization)
        form_keyword = OperationKeywordForm()
        form_einsatzort = OperationPropertyLocationForm()

    return render(request, 'pager/operation_create_form.html', {'form': form_op,
                                                                'form_keyword': form_keyword,
                                                                'form_einsatzort': form_einsatzort,
                                                                'organization': organization})


@login_required
def operationResend(request, pk):
    if not settings.DEBUG:
        raise Http404()

    alarm = Operation.objects.get(pk=pk)
    send_alarm(None, alarm, True)

    messages.add_message(request, messages.SUCCESS, 'Operation "{0}" erneut gesendet'.format(alarm.keywords))

    return redirect('pager:operation-list')


class OperationDeleteView(DeleteView):
    model = Operation
    success_url = reverse_lazy('pager:operation-list')

    def get_queryset(self):
        return super().get_queryset().filter(organization__owner=self.request.user)


class DeviceIndexView(LoginRequiredMixin, ListView):
    context_object_name = 'device_list'
    model = Device

    def get_queryset(self):
        """Return the last five published questions."""
        return super().get_queryset().filter(owner=self.request.user.id)


class DeviceDetailView(LoginRequiredMixin, DetailView):
    model = Device

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user.id)


class DeviceDeleteView(DeleteView):
    model = Device
    success_url = reverse_lazy('pager:device-list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user.id)
