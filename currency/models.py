from django.db import models


class Currency(models.Model):
    CURRENCY = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    ]
    created_at = models.DateTimeField(auto_now=True)
    currency = models.CharField(max_length=5, choices=CURRENCY)
    source = models.CharField(max_length=50)
    buy_price = models.DecimalField(max_digits=15, decimal_places=6)
    sell_price = models.DecimalField(max_digits=15, decimal_places=6)

    class Meta:
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return f"{self.created_at}, {self.currency}, {self.source}, BUY {self.buy_price}, SELL {self.sell_price}"
