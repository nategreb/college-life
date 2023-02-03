from django.forms import ChoiceField

from .widgets import CustomDataList


class DatalistField(ChoiceField):
    widget = CustomDataList
    default_error_messages = {
        'invalid_choice': 'Select a valid choice. %(value)s is not one of the available choices.',
    }

    def __init__(self, *, choices='', **kwargs):
        super().__init__(**kwargs)
        self.choices = choices
