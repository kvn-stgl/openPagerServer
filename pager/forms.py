import uuid
from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from pager.models import Operation, Organization, OperationKeywords, OperationPropertyLocation


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

            self.user.organization = organization
            self.user.save()

        return organization

    class Meta:
        model = Organization
        fields = ['name', 'address', 'plz', 'place']


class OperationCreateForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, organization, *args, **kwargs):
        self.organization = organization
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        operation = super().save(False)
        operation.operation_guid = uuid.uuid4()
        operation.timestamp = datetime.now()
        operation.organization = self.organization

        if commit:
            operation.save()

        return operation

    class Meta:
        model = Operation
        fields = ['messenger', 'comment']


class OperationPropertyLocationForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = OperationPropertyLocation
        fields = ['geo_latitude', 'geo_longitude', 'street', 'street_number', 'zip_code', 'city']


class OperationKeywordForm(ModelForm):
    required_css_class = 'required'

    class Meta:
        model = OperationKeywords
        fields = ['emergency_keyword', 'keyword']


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

        if user.organization == self.organization:
            raise ValidationError(_('Benutzer ist bereits Mitglied'))

        return user
