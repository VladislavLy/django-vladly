from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Logger, Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'age', 'phone', 'show_in_the_group_url', 'group_id')
    list_filter = ('name', 'surname', 'age')
    search_fields = ('name__startswith', 'surname__startswith', 'age__iexact')
    list_display_links = ('name', 'surname', 'show_in_the_group_url')
    empty_value_display = '-empty-'

    def group_id(self, obj):
        try:
            return f"Group ID: {obj.in_the_group.id}"
        except AttributeError:
            pass
    group_id.short_description = 'Group ID'

    def group_name(self, obj):
        try:
            return obj.in_the_group.subject
        except AttributeError:
            pass
    group_name.short_description = 'Group name'

    def show_in_the_group_url(self, obj):
        if obj.in_the_group is not None:
            link = reverse("admin:groups_group_change", args=[obj.in_the_group.id])
            return format_html(f"<a href='{link}'>{obj.in_the_group.subject}</a>")
        else:
            pass

    show_in_the_group_url.short_description = "Subject"


@admin.register(Logger)
class LoggerAdmin(admin.ModelAdmin):
    list_display = ('method', 'path', 'execution_time', 'created')
