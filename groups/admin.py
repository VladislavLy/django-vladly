from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'ratio_of_students', 'show_teacher_url', 'get_id_teacher',)
    list_filter = ('subject', 'ratio_of_students', 'main_teacher')
    search_fields = ('subject__startswith', 'ratio_of_students__iexact')
    list_display_links = ('subject', 'show_teacher_url')
    empty_value_display = '-empty-'

    def get_teacher(self, obj):
        try:
            return f"{obj.main_teacher.name}"
        except AttributeError:
            pass
    get_teacher.short_description = 'Main teacher'

    def get_id_teacher(self, obj):
        try:
            return f"Teacher ID: {obj.main_teacher.id}"
        except AttributeError:
            pass
    get_id_teacher.short_description = 'Teacher ID'

    def show_teacher_url(self, obj):
        if obj.main_teacher is not None:
            link = reverse("admin:teachers_teacher_change", args=[obj.main_teacher.id])
            return format_html(f"<a href='{link}'>{obj.main_teacher.name}</a>")
        else:
            pass

    show_teacher_url.short_description = "Main teacher"
