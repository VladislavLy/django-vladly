from django.shortcuts import render

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
