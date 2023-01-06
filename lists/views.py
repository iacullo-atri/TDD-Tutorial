from django.shortcuts import render, redirect
from django.urls import reverse

from lists.models import Item, List

def index(request):
    return render(request, 'lists/index.html')

def view_list(request, list_id):
    target_list = List.objects.get(id=list_id)
    context = { 'list': target_list }
    return render(request, 'lists/list.html', context)

def new_list(request):
    new_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=new_list)
    return redirect('lists:view_list', list_id=new_list.id)

def add_item(request, list_id):
    target_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=target_list)
    return redirect('lists:view_list', list_id=target_list.id)