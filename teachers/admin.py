from django.contrib import admin

from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'age', 'subject_class')
    list_filter = ('name', 'surname', 'age', 'subject_class')
    search_fields = ('name__startswith', 'surname__startswith', 'age__iexact')
    list_display_links = ('name', 'surname')
    empty_value_display = '-empty-'
