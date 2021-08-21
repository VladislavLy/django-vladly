from django.contrib import admin

from .models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('subject', 'ratio_of_students')
    list_filter = ('subject', 'ratio_of_students')
    search_fields = ('subject__startswith', 'ratio_of_students__iexact')
    list_display_links = ('subject',)
