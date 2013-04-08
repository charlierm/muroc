from django.forms import ModelForm
from core.models import Case
from django.forms import forms


class CaseForm(ModelForm):
    class Meta:
        model = Case
        widgets = {
        }

    def __init__(self, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['cols'] = 100

