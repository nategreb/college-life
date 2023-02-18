from django import forms

from colleges.models import ResidentialArea, Dorms, RequestProfessor, CollegeCourse, RequestCourse
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


class RequestCourseForm(forms.ModelForm):
    class Meta:
        model = RequestCourse
        fields = ['college', 'department', 'course_id', 'course_name']

    def clean(self):
        cleaned_data = super(RequestCourseForm, self).clean()
        # string cleanup
        cleaned_data['course_id'] = cleaned_data['course_id'].upper()
        cleaned_data['course_name'] = cleaned_data['course_name'].lower()
        return cleaned_data


class RequestProfessorForm(forms.ModelForm):
    class Meta:
        model = RequestProfessor
        fields = ['college', 'department', 'first_name', 'last_name', 'courses']

    def clean(self):
        cleaned_data = super(RequestProfessorForm, self).clean()
        # string cleanup
        cleaned_data['first_name'] = cleaned_data['first_name'].capitalize()
        cleaned_data['last_name'] = cleaned_data['last_name'].capitalize()
        return cleaned_data

