from celery import shared_task

import requests

from .models import Currency


@shared_task
def get_currency_rate():
    codes_ISO_4217 = (840, 978)
    responce_exchange_rate_monobank = requests.get('https://api.monobank.ua/bank/currency')
    responce_exchange_rate_nationalbank = requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json')

    if responce_exchange_rate_monobank.status_code == 200:
        for rate in responce_exchange_rate_monobank.json():
            if rate.get('currencyCodeA') not in codes_ISO_4217 or rate.get('currencyCodeB') in codes_ISO_4217:
                continue
            elif rate.get('currencyCodeA') == codes_ISO_4217[0]:
                code = 'USD'
            elif rate.get('currencyCodeA') == codes_ISO_4217[1]:
                code = 'EUR'
            currency_monobank = Currency(
                currency=str(code),
                source='Monobank',
                buy_price=rate.get('rateBuy'),
                sell_price=rate.get('rateSell')
            )
            currency_monobank.save()

    if responce_exchange_rate_nationalbank.status_code == 200:
        for rate in responce_exchange_rate_nationalbank.json():
            if rate.get('cc') not in [currency[0] for currency in Currency.CURRENCY]:
                continue
            else:
                currency_nationalbank = Currency(
                    currency=rate.get('cc'),
                    source='National Bank',
                    buy_price=rate.get('rate'),
                    sell_price=rate.get('rate')
                )
            currency_nationalbank.save()

    return 'Currency exchange was saved!'
