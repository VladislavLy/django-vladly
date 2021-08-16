from django.urls import path

from . import views


urlpatterns = [
    path('groups/', views.groups_db, name='groups_db'),
    path('list-of-groups/', views.list_of_groups, name='list_of_groups'),
    path('create-group/', views.create_group, name='create_group'),


]
