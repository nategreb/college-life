from django import forms

from colleges.models import ResidentialArea, Dorms, Professor
from templates.django.forms.fields import DatalistField
from templates.django.forms.widgets import CustomDataList


class NewResidentialAreaForm(forms.ModelForm):
    class Meta:
        model = ResidentialArea
        fields = ['res_hall_name']


class NewDorm(forms.ModelForm):
    class Meta:
        model = Dorms
        fields = ['dorm_name']


class SearchForm(forms.Form):
    search = DatalistField(widget=CustomDataList(attrs={'class': 'autoComplete'}))
