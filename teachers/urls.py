from django.urls import path
from . import views


urlpatterns = [
    path('teachers/', views.generate_teachers, name='generate_teachers'),

]
