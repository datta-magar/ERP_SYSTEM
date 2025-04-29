from django.contrib import admin
from .models import Item
from .models import StockTransaction

admin.site.register(Item)
admin.site.register(StockTransaction)