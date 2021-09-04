from django.contrib import admin

from .models import Logger, Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'age')
    list_filter = ('name', 'surname', 'age')
    search_fields = ('name__startswith', 'surname__startswith', 'age__iexact')
    list_display_links = ('name', 'surname')


@admin.register(Logger)
class LoggerAdmin(admin.ModelAdmin):
    list_display = ('method', 'path', 'execution_time', 'created')
