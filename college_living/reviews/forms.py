"""Forms for the ``reviews`` app."""
from django import forms
from django.conf import settings

from django_libs.loaders import load_member
from django.contrib.contenttypes.models import ContentType

from .models import Review, Rating, RatingCategory


class ReviewForm(forms.ModelForm):
    def __init__(self, reviewed_item, user=None, *args, **kwargs):
        self.user = user
        self.reviewed_item = reviewed_item
        self.content_type = ContentType.objects.get_for_model(reviewed_item)
        self.widget = load_member(
            getattr(settings, 'REVIEW_FORM_CHOICE_WIDGET',
                    'django.forms.widgets.Select')
        )()
        super(ReviewForm, self).__init__(*args, **kwargs)
        # Dynamically add fields for each rating category
        for category in RatingCategory.objects.filter(content_type=self.content_type):
            field_name = 'category_{0}'.format(category.pk)
            choices = category.get_choices()
            self.fields[field_name] = forms.ChoiceField(
                choices=choices, label=category.name,
                help_text=category.question,
                widget=self.widget,
            )
            self.fields[field_name].required = category.required
            if self.instance.pk:
                try:
                    self.initial.update({
                        'category_{0}'.format(category.pk): Rating.objects.get(
                            review=self.instance, category=category).value,
                    })
                except Rating.DoesNotExist:
                    pass

    def save(self, *args, **kwargs):
        if not self.instance.pk:
            self.instance.user = self.user
            self.instance.reviewed_item = self.reviewed_item
            self.instance.content_type = self.content_type
        self.instance = super(ReviewForm, self).save(*args, **kwargs)
        # Update or create ratings
        for field in self.fields:
            if field.startswith('category_'):
                rating, created = Rating.objects.get_or_create(
                    review=self.instance,
                    category=RatingCategory.objects.get(
                        pk=field.replace('category_', ''),
                    ),
                    content_type=self.instance.content_type,
                    object_id=self.instance.reviewed_item.id
                )
                rating.value = self.cleaned_data[field]
                rating.save()

        self.instance.average_rating = self.instance.get_average_rating()
        self.instance.save()
        return self.instance

    class Meta:
        model = Review
        fields = ('content',)
