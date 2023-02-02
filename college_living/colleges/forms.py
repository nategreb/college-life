# from dal import autocomplete

from django import forms
from colleges.models import ResidentialArea, College, Dorms, Professor


class NewResidentialAreaForm(forms.ModelForm):
    class Meta:
        model = ResidentialArea
        fields = ['res_hall_name']


class NewDorm(forms.ModelForm):
    class Meta:
        model = Dorms
        fields = ['dorm_name']


class SearchForm(forms.ModelForm):
    """
    - get contentype of request
    - search for objects in the table

    """
    pass
