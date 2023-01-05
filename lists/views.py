from django.shortcuts import render, redirect
from django.urls import reverse

from lists.models import Item, List

def index(request):
    return render(request, 'lists/index.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})

def new_list(request):
    new_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=new_list)
    return redirect('lists:view_list')