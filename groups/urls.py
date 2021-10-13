from django.urls import path

from . import views


urlpatterns = [
    path('groups-generate/', views.groups_db, name='groups_db'),
    path('list-of-groups/', views.list_of_groups, name='list_of_groups'),
    path('create-group/', views.create_group, name='create_group'),
    path('edit-group/<int:group_id>/', views.edit_group, name='edit_group'),
    path('delete-group/<int:group_id>/', views.delete_group, name='delete_group'),

]
