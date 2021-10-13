from django.shortcuts import render
from django.views.generic import ListView

from .models import Currency


def currency_rate_list(request):
    result = []
    count = 0
    for i in Currency.objects.order_by('-created_at'):
        result.append(i)
        count += 1
        if count == 4:
            break
    return render(request, 'currency/currency_rate.html', {"Title": 'Currency', 'object_list': result})


class CurrencyRateList(ListView):
    model = Currency
    template_name = 'currency/currency_rate.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['Title'] = 'Currency'
        return data

    def get_queryset(self):
        result = []
        count = 0
        for i in Currency.objects.order_by('-created_at'):
            result.append(i)
            count += 1
            if count == 4:
                break
        return result
