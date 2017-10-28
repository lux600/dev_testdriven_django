from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ValidationError

from lists.models import Item, List

# Create your views here.
def home_page(request):
    return render(request, 'lists/home.html')

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'lists/list.html', { 'list': list_ })

def new_list(request):
    list_ = List.objects.create()
    text = request.POST['item_text']
    # Item.objects.create(text=text, list= list_)
    item = Item(text=text, list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "빈 아이템을 등록할 수 없습니다"
        return render(request, 'lists/home.html', {"error": error})

    return redirect('/lists/%d/' % (list_.id))
    # return redirect(list_)


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    text = request.POST['item_text']
    # Item.objects.create(text=text, list=list_)
    item = Item(text=text, list=list_)

    try:
        item.full_clean()
        item.save()

    except ValidationError:
        # list_.delete()
        error = "빈 아이템을 등록할 수 없습니다"
        return render(request, 'lists/list.html', {'list': list_, 'error': error})

    return redirect('/lists/%d/' % (list_.id,))