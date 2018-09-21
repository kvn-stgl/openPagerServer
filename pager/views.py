from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView

from pager.forms import CustomOrganizationCreateForm, MembershipAddForm, AlarmCreateForm
from pager.models import Alarm, Device, Organization, Membership


class OrganizationIndexView(LoginRequiredMixin, ListView):
    context_object_name = 'organization_list'
    model = Organization

    def get_queryset(self):
        """Return the last five published questions."""
        return super().get_queryset() \
            .annotate(num=Count('name')) \
            .filter(membership__user=self.request.user) \
            .order_by('owner')


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    form_class = CustomOrganizationCreateForm
    template_name = 'pager/organization_create_form.html'
    success_url = reverse_lazy('pager:organization-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class OrganizationDeleteView(DeleteView):
    model = Organization
    success_url = reverse_lazy('pager:organization-list')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    model = Organization
    form_class = MembershipAddForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = Membership.objects.filter(organization=self.object).prefetch_related('user')
        return context

    def get_queryset(self):
        return super().get_queryset().annotate(num=Count('name')).filter(membership__user=self.request.user)


@login_required
def membershipAdd(request, pk):
    organization = get_object_or_404(Organization, pk=pk)

    if organization.owner_id != request.user.id:
        raise Http404('No matches the given query.')

    if request.method == "POST":
        form = MembershipAddForm(organization, request.POST)
        if form.is_valid():
            new_user = form.cleaned_data['user']
            Membership.objects.create(organization=organization, user=new_user, is_member=True)
            return redirect('pager:organization-detail', pk=pk)
    else:
        form = MembershipAddForm(organization)

    return render(request, 'pager/membership_add_form.html', {'form': form, 'organization': organization})


class MembershipLeaveView(DeleteView):
    model = Membership
    success_url = reverse_lazy('pager:organization-list')
    template_name_suffix = '_confirm_leave'

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return super().get_queryset() \
            .filter(user=self.request.user, organization__id=pk) \
            .exclude(organization__owner=self.request.user) \
            .get()


class MembershipDeleteView(DeleteView):
    model = Membership

    def get_queryset(self):
        return super().get_queryset().filter(organization__owner=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy('pager:organization-detail', kwargs={'pk': self.get_object().organization.id})


class AlarmIndexView(LoginRequiredMixin, ListView):
    context_object_name = 'alarm_list'
    model = Alarm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['organization'] = Organization.objects.get(pk=self.kwargs.get('pk'))
        return context

    def get_queryset(self):
        """Return the last five published questions."""
        organization_id = self.kwargs.get('pk')
        return super().get_queryset() \
            .filter(organization=organization_id) \
            .filter(organization__membership__user=self.request.user) \
            .order_by('-time')


class AlarmDetailView(LoginRequiredMixin, DetailView):
    model = Alarm

    def get_queryset(self):
        return super().get_queryset().filter(organization__membership__user=self.request.user) \
            .prefetch_related('organization')


@login_required
def alarmCreate(request, pk):
    organization = get_object_or_404(Organization, pk=pk)

    if organization.owner_id != request.user.id:
        raise Http404('No matches the given query.')

    if request.method == "POST":
        form = AlarmCreateForm(organization, request.POST)
        if form.is_valid():
            alarm = form.save()
            return redirect('pager:alarm-detail', pk=alarm.id)
    else:
        form = AlarmCreateForm(organization)

    return render(request, 'pager/alarm_create_form.html', {'form': form, 'organization': organization})


class AlarmDeleteView(DeleteView):
    model = Alarm
    success_url = reverse_lazy('pager:alarm-list')

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
