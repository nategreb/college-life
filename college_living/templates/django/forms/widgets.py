from django.forms import Select


class CustomDataList(Select):
    input_type = 'text'
    template_name = 'django/forms/widgets/datalist.html'
    option_template_name = 'django/forms/widgets/datalist_option.html'
    add_id_index = False
    checked_attribute = {'selected': True}
    option_inherits_attrs = False
