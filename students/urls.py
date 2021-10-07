from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('generate-student/', views.GenerateStudent.as_view(), name='generate_student'),
    path('generate-students/', views.GenerateStudents.as_view(), name='generate_students'),
    path('generate-students-count/<number>', views.GenerateStudentsCount.as_view(), name='generate_students_count'),
    path('list-of-students/', views.ListOfStudents.as_view(), name='list_of_students'),
    path('create-student/', views.CreateStudent.as_view(), name='create_student'),
    path('edit-student/<int:pk>/', views.EditStudent.as_view(), name='edit_student'),
    path('delete-student/<int:pk>/', views.DeleteStudent.as_view(), name='delete_student'),

]
