from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login # 로그인 및 회원가입 기능을 구현하기 위한 패키지
from .crawling import Crawling
from .models import Menu, Rest, RestMenu
from .forms import MenuForm, RestForm, RestMenuForm, UserForm
import math
from haversine import haversine  # haversine 은 위도 경도로 거리 계산 함수
# pip install haversine 이 필요하다

def main(request):  # 회원, 비회원을 구분하는 페이지
    return render(request, 'bootrc/main_page.html')

"""def login(request):  # 회원(또는 가입) 로그인 페이지
    return render(request, 'bootrc/login.html')"""

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

def recommendmenu(request):
    restmenu_list = RestMenu.objects.order_by('-recommendmenu')
    context = {'restmenu_list': restmenu_list}
    return render(request, 'bootrc/recommend_list.html', context)


def crawling(request):
    Crawling()
    return redirect('bootrc:index')

def restmenu_list(request, rest_rest_num):
    rest = get_object_or_404(Rest, pk=rest_rest_num)
    restmenu_list = RestMenu.objects.filter(rest_id=rest.rest_num) #RestMenu의 멤버 rest_id는 = rest객체의 rest_num
    context = {'rest': rest,'restmenu_list': restmenu_list}
    return render(request, 'bootrc/restmenu_list.html', context)


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
    가게 등록, 거리 계산 입력
    '''
    if request.method == 'POST':
        form = RestForm(request.POST)
        if form.is_valid():
            menu = form.save()
            menu.save()
            rest_n = Rest.objects.all()
            school_bd = (35.817094, 127.090152)  # 학교 후문의 위도 경도
            destination = (rest_n.rest_location_lat, rest_n.rest_location_lon)  # 목적지 위도 경도
            distance = haversine(school_bd, destination, unit='m')
            result = int(distance)
            # haversine 은 위도 경도로 거리 계산 함수 from haversine, unit 은 거리 표현 방법
            Rest.rest_distance_fromBD = result
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
            restmenu.recommend_calc()
            restmenu.save()
            return redirect('bootrc:restmenu_list', rest_rest_num)
    else:
        form = RestMenuForm()
    rest_menu = {'rest': rest, 'form': form}
    return render(request, 'bootrc/restmenu_form.html', rest_menu)


# 회원가입 가능 구현
def signup(request):
    if request.method == "POST":  # 요청받은 방식이 POST 방식이 아닌 경우, 회원가입 페이지로 이동함.
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # authenticate 함수는 사용자명과 비밀번호가 일치하는지 검증해 줌.

            login(request, user)  # 로그인
            return redirect('bootrc:menu_select')  # 가입 완료 후, 메인 페이지로 이동함.
    else:
        form = UserForm()
    return render(request, 'bootrc/signup.html', {'form': form})


def menu_favorite(request):  # 음식 선호도 조사
    menu_list = Menu.objects.order_by('menu_num')
    current_user = request.user
    context = {'menu_list': menu_list}
    return render(request, 'bootrc/menu_list_favorite_select.html', context)


def menu_delete(request, menu_menu_num):
    '''
    질문삭제
    '''
    menu = get_object_or_404(Menu, pk=menu_menu_num)
    menu.delete()
    return redirect('bootrc:menu_list')

def rest_delete(request, rest_rest_num):
    '''
    메뉴삭제
    '''
    rest = get_object_or_404(Rest, pk=rest_rest_num)
    rest.delete()
    return redirect('bootrc:rest_list')

def restmenu_delete(request, restmenu_id):
    '''
    가게메뉴삭제
    '''
    restmenu = get_object_or_404(RestMenu, pk=restmenu_id)
    restmenu.delete()
    #return redirect('bootrc:restmenu_list restmenu.rest.rest_num')
    return redirect('bootrc:rest_list')


