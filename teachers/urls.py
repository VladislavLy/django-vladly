from django.urls import path, re_path

from . import views


urlpatterns = [
    path('teachers/', views.generate_teachers, name='generate_teachers'),
    path('list-of-teachers/', views.list_of_teachers, name='list_of_teachers'),
    re_path(r'^list-of-teachers/(?P<name>\D+)/(?P<age>\d+)$', views.list_of_teachers_param, name='list_of_teachers_param'),
    re_path(r'^list-of-teachers/(?P<name>\D+)/(?P<surname>\D+)$', views.list_of_teachers_param, name='list_of_teachers_param'),
    re_path(r'^list-of-teachers/(?P<name>\D+)|(?P<age>\d+)$', views.list_of_teachers_param, name='list_of_teachers_param'),

]
