"""Admin classes for the reviews app."""
from django.contrib import admin

from . import models


class RatingAdmin(admin.ModelAdmin):
    list_display = ['review', 'category', 'value', ]
    raw_id_fields = ['review', ]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewed_item', 'user', 'language', 'creation_date']


class ReviewExtraInfoAdmin(admin.ModelAdmin):
    list_display = ['type', 'review', 'content_object']


class ReviewCategoryChoiceAdmin(admin.ModelAdmin):
    list_display = ['ratingcategory', 'value', 'get_label']
    list_select_related = []

    def get_label(self, obj):
        return obj.label

    get_label.short_description = 'Label'


admin.site.register(models.Rating, RatingAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.RatingCategory)
admin.site.register(models.ReviewExtraInfo, ReviewExtraInfoAdmin)
admin.site.register(models.RatingCategoryChoice, ReviewCategoryChoiceAdmin)
