from django.shortcuts import render, get_object_or_404, redirect
from .models import Menu, Rest, RestMenu
from .forms import MenuForm, RestForm, RestMenuForm
import math

def main(request):  # 회원, 비회원을 구분하는 페이지
    return render(request, 'bootrc/main_page.html')

def login(request):  # 회원(또는 가입) 로그인 페이지
    return render(request, 'bootrc/login.html')

def index(request):  # 버튼 메뉴들이 있는 메인 페이지
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
    restmenu_list = RestMenu.objects.filter(rest_id=rest.rest_num) #RestMenu의 멤버 rest_id는 = rest객체의 rest_num
    context = {'rest': rest,'restmenu_list': restmenu_list}
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
    가게 등록
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
            return redirect('bootrc:restmenu_list', rest_rest_num)
    else:
        form = RestMenuForm()
    rest_menu = {'rest': rest, 'form': form}
    return render(request, 'bootrc/restmenu_form.html', rest_menu)

# 테스트 해봐야 함
def distance_from_college(request, rest_rest_num):
    """
    학교에서 가게 위치 거리 계산
    전주대 후문 위도 경도 : 35.817094, 127.090152 lat
    전주대 정문 위도 경도 : 35.813841, 127.094034 lon
    """
    rest_location = rest_rest_num
    if request.method == 'POST':
        rest_location_lat = rest_location.rest_location_lat
        rest_location_lon = rest_location.rest_location_lon
        distance = math.sqrt((35.817094-rest_location_lat)+(35.813841-rest_location_lon))
#    return render(request, 'bootrc/rest_list.html', {'distance': distance})
    return render(request, 'bootrc/rest_list.html', {'distance': 4})

