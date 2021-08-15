from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('generate-student/', views.generate_student, name='generate_student'),
    path('generate-students/', views.generate_students, name='generate_students'),
    path('generate-students-count/<number>', views.generate_students_count, name='generate_students_count'),

]