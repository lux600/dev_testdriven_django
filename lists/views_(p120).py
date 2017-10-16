from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

from lists.models import Item, List

# Create your views here.
def home_page(request):
    return render(request, 'lists/home.html')

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'lists/list.html', {'items': items})

def new_list(request):
    list_ = List.objects.create()
    text = request.POST['item_text']
    Item.objects.create(text=text, list= list_)
    return redirect('/lists/the-only-list-in-the-world/')