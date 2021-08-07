from django.urls import path
from . import views


urlpatterns = [
    path('groups/', views.groups_db, name='groups_db'),

]
