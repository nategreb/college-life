from django import forms
from django.forms import ModelForm

from .models import CourseReview

from colleges.models.courses import SemesterYear


class AddCourseReviewForm(ModelForm):
    comment = forms.CharField(max_length=160, widget=forms.Textarea())
    term = forms.ModelChoiceField(queryset=SemesterYear.objects.all())
    test_heavy = forms.IntegerField(min_value=1, max_value=5)
    usefulness = forms.IntegerField(min_value=1, max_value=5)
    theoretical = forms.IntegerField(min_value=1, max_value=5)
    take_again = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = CourseReview
        fields = ['comment', 'term', 'test_heavy', 'usefulness', 'theoretical', 'take_again']
