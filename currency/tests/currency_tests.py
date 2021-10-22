from django.test import Client

import pytest

from pytest_django.asserts import assertTemplateUsed

from ..models import Currency
from ..tasks import get_currency_rate


@pytest.mark.django_db
def test_get_currency():
    x = Currency(
        currency='USD',
        source='some_bank',
        buy_price=27.01,
        sell_price=29.01,
    )
    x.save()
    assert Currency.objects.all().count() == 1
    assert Currency.objects.get(id=1).currency == 'USD'
    assert 'bank' in Currency.objects.last().__str__()
    response = Client().get('/currency')
    assertTemplateUsed(response, 'currency/currency_rate.html')


@pytest.mark.django_db
def test_get_currency_task():
    assert get_currency_rate() == 'Currency exchange was saved!'


@pytest.mark.django_db
def test_get_currency_responce():
    x = Currency(
        currency='USD',
        source='some_bank',
        buy_price=27.01,
        sell_price=29.01,
    )
    x.save()
    c = Client()
    x = c.get("/currency")
    assert x.status_code == 200
