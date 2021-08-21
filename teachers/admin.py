from django.contrib import admin

from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'age')
    list_filter = ('name', 'surname', 'age')
    search_fields = ('name__startswith', 'surname__startswith', 'age__iexact')
    list_display_links = ('name', 'surname')
