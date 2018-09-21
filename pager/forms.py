from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _

from pager.models import Alarm, Organization, Membership


class CustomOrganizationCreateForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        organization = super().save(False)
        organization.owner = self.user

        if commit:
            organization.save()
            Membership.objects.create(user=self.user, organization=organization, is_member=True)

        return organization

    class Meta:
        model = Organization
        fields = ['name', 'address']


class AlarmCreateForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, organization, *args, **kwargs):
        self.organization = organization
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        alarm = super().save(False)
        alarm.organization = self.organization

        if commit:
            alarm.save()

        return alarm

    class Meta:
        model = Alarm
        fields = ['title', 'message', 'destination', 'destination_lat', 'destination_lng']


class MembershipAddForm(forms.Form):
    required_css_class = 'required'

    user = forms.EmailField(help_text="E-Mail des Mitglieds", label="Mitglied")

    def __init__(self, organization, *args, **kwargs):
        self.organization = organization
        super().__init__(*args, **kwargs)

    def clean_user(self):
        data = self.cleaned_data['user']

        user = get_user_model().objects.filter(email=data).first()

        if user is None:
            raise ValidationError(_('Benutzer nicht gefunden'))

        exist_user = Membership.objects.filter(organization=self.organization, user=user).first()
        if exist_user != None:
            raise ValidationError(_('Benutzer ist bereits Mitglied'))

        return user