from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('generate-student/', views.generate_student, name='generate_student'),
    path('generate-students/', views.generate_students, name='generate_students'),
    path('generate-students-count/<number>', views.generate_students_count, name='generate_students_count'),
    path('list-of-students/', views.list_of_students, name='list_of_students'),
    path('create-student/', views.create_student, name='create_student'),
    path('edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),

]
