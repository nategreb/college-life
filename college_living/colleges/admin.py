from django.contrib import admin

# Register your models here.
"""Admin classes for the reviews app."""
from django.contrib import admin

from . import models


class ProfessorAdmin(admin.ModelAdmin):
    pass


class CourseAdmin(admin.ModelAdmin):
    pass


class CollegeAdmin(admin.ModelAdmin):
    pass


class DepartmentAdmin(admin.ModelAdmin):
    pass


class RequestCoursesAdmin(admin.ModelAdmin):
    pass


class RequestProfessorAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.College, ProfessorAdmin)
admin.site.register(models.Professor, CourseAdmin)
admin.site.register(models.CollegeCourse, CollegeAdmin)
admin.site.register(models.Department, CollegeAdmin)
admin.site.register(models.RequestProfessor, CollegeAdmin)
admin.site.register(models.RequestCourse, CollegeAdmin)
