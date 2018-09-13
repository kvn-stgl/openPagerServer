from django.forms import ModelForm

from pager.models import Alarm


class CustomAlarmCreateForm(ModelForm):

    class Meta:
        model = Alarm
        fields = '__all__'  # ['title', 'message']
