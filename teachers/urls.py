from django.urls import path, re_path

from . import views


urlpatterns = [
    path('generate-teachers/', views.GenerateTeachers.as_view(), name='generate_teachers'),
    path('list-of-teachers/', views.ListOfTeachers.as_view(), name='list_of_teachers'),
    re_path(r'^list-of-teachers/(?P<name>\D+)/(?P<age>\d+)$', views.ListOfTeachers.as_view(), name='list_of_teachers_param'),
    re_path(r'^list-of-teachers/(?P<name>\D+)/(?P<surname>\D+)$', views.ListOfTeachers.as_view(), name='list_of_teachers_param'),
    re_path(r'^list-of-teachers/(?P<name>\D+)|(?P<age>\d+)$', views.ListOfTeachers.as_view(), name='list_of_teachers_param'),
    path('create-teacher/', views.CreateTeacher.as_view(), name='create_teacher'),
    path('edit-teacher/<int:pk>/', views.EditTeacher.as_view(), name='edit_teacher'),
    path('delete-teacher/<int:pk>/', views.DeleteTeacher.as_view(), name='delete_teacher'),

]
