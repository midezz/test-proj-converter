from django.contrib import admin
from django.contrib.admin import ModelAdmin
from exchange.models import Rate


class AdminRate(ModelAdmin):
    model = Rate
    list_display = ['name', 'code', 'exchange_rate', 'updated_at']


admin.site.register(Rate, AdminRate)
