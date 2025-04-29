from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Item

@login_required
def item_list(request):
    items = Item.objects.all()
    return render(request, 'inventory/item_list.html', {'items': items})
