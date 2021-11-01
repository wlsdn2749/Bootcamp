from django.shortcuts import render, get_object_or_404, redirect
from .models import Menu, Rest, RestMenu
from .forms import MenuForm, RestForm, RestMenuForm

def index(request):
    return render(request, 'bootrc/main.html')

def menu_list(request):
    menu_list = Menu.objects.order_by('menu_num')
    context = {'menu_list': menu_list}
    return render(request, 'bootrc/menu_list.html', context)

def rest_list(request):
    rest_list = Rest.objects.order_by('rest_num')
    context = {'rest_list': rest_list}
    return render(request, 'bootrc/rest_list.html', context)

def restmenu_list(request, rest_rest_num):
    rest = get_object_or_404(Rest, pk=rest_rest_num)
    restmenu_list = RestMenu.objects.order_by('rest_id')
    context = {'restmenu_list': restmenu_list}
    return render(request, 'bootrc/restmenu_list.html', context) # 수정해야함 이부분

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

def restmenu_create(request, rest_rest_num):
    '''
    레스토랑 메뉴 등록
    '''
    rest = get_object_or_404(Rest, pk=rest_rest_num)
    if request.method == 'POST':
        form = RestMenuForm(request.POST)
        if form.is_valid():
            restmenu = form.save(commit=False)
            restmenu.rest = rest
            restmenu.save()
            return redirect('bootrc:index')
    else:
        form = RestMenuForm()
    rest_menu = {'rest': rest, 'form': form}
    return render(request, 'bootrc/restmenu_form.html', rest_menu)
