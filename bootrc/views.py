from django.shortcuts import render, get_object_or_404, redirect
from .models import Menu, Rest
from .forms import MenuForm, RestForm

def index(request):
    return render(request, 'bootrc/main.html')

def menu_list(request):
    menu_list = Menu.objects.order_by('-menu_num')
    context = {'menu_list': menu_list}
    return render(request, 'bootrc/menu_list.html', context)

def rest_list(request):
    rest_list = Rest.objects.order_by('-rest_num')
    context = {'rest_list': rest_list}
    return render(request, 'bootrc/rest_list.html', context)

def menu_create(request):
    '''
    메뉴 등록
    '''
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            menu.save()
            return redirect('bootrc:index')
    else:
        form = MenuForm()
    return render(request, 'bootrc/menu_form.html', {'form': form})

def rest_create(request):
    '''
    메뉴 등록
    '''
    if request.method == 'POST':
        form = RestForm(request.POST)
        if form.is_valid():
            menu = form.save()
            menu.save()
            return redirect('bootrc:index')
    else:
        form = RestForm()
    return render(request, 'bootrc/rest_form.html', {'form': form})
