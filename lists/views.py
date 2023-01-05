from django.shortcuts import render, redirect
from django.urls import reverse

from lists.models import Item

def index(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect(reverse('lists:index'))

    items = Item.objects.all()
    return render(request, 'lists/index.html', {'items': items})
