"""Forms for the ``test_app`` app."""
from django import forms

from reviews.forms import ReviewForm
from reviews.models import ReviewExtraInfo
from .models import WeatherCondition


class CustomReviewForm(ReviewForm):
    """Form to make use of the reviews extra info."""

    def __init__(self, reviewed_item, user=None, *args, **kwargs):
        super(CustomReviewForm, self).__init__(
            reviewed_item, user, *args, **kwargs)
        choices = [(x.pk, x.name) for x in WeatherCondition.objects.all()]
        self.fields['weather_conditions'] = forms.fields.ChoiceField(
            choices=choices)

    def save(self, *args, **kwargs):
        self.instance = super(CustomReviewForm, self).save(*args, **kwargs)
        ReviewExtraInfo.objects.create(
            type='weather_conditions',
            review=self.instance,
            content_object=WeatherCondition.objects.get(
                pk=self.cleaned_data['weather_conditions']),
        )
        return self.instance
