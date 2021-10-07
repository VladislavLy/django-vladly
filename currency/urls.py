from django.urls import path

from . import views


urlpatterns = [
    path('currency', views.CurrencyRateList.as_view(), name='currency_rate_list'),

]
