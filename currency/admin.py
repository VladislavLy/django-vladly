from django.contrib import admin

from .models import Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("created_at", "currency", "source", "buy_price", "sell_price")
    list_filter = ("created_at", "source", "currency", )
    search_fields = ("source",)
