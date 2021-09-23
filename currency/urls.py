from django.urls import path

from . import views


urlpatterns = [
    path('currency', views.currency_rate_list, name='currency_rate_list'),

]
