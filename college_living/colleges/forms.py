from django import forms
from colleges.models import ResidentialArea, College, Dorms


class NewResidentialAreaForm(forms.ModelForm):
    class Meta:
        model  = ResidentialArea
        fields = ['res_hall_name']

class NewDorm(forms.ModelForm):
    class Meta:
        model  = Dorms
        fields = ['dorm_name']