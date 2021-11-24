from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login # 로그인 및 회원가입 기능을 구현하기 위한 패키지
from .crawling import Crawling
from django.contrib.auth.decorators import login_required
from .models import Menu, Rest, RestMenu, Review, Prefer, Categories, recentRecommended, AppReview, PreferCate
from .forms import MenuForm, RestForm, RestMenuForm, UserForm, PreferForm, recentRecommendedForm, AppReviewForm
from django.contrib.auth.models import User
from time import *
from datetime import *
import random
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
    categories = Categories.objects.all()
    context = {'rest_list': rest_list, 'categories':categories}
    return render(request, 'bootrc/rest_list.html', context)

def recommendmenu(request):
    #restmenu = RestMenu.objects.order_by('-recommendmenu').first() #점수가 높은순 1개만 확인
    restmenu = RestMenu.objects.order_by('?').first() # 랜덤정렬 첫번째
    review = Review.objects.filter(restaurant_id=restmenu.rest_id).order_by('?').first()
    context = {'restmenu': restmenu, 'review': review}
    return render(request, 'bootrc/recommend_list.html', context)

def recommendmenu2(request):
    if request.method == 'POST':
        form = recentRecommendedForm(request.POST)
        if form.is_valid():
            recommend = form.save(commit=False)
            recommend.user = request.user
            recommend.save()
            return redirect('bootrc:index')
    else:
        form = recentRecommendedForm()

    current_user = request.user
    cate_list = PreferCate.objects.filter(user_num=current_user).order_by('-id')
    menu = recom_menu(cate_list, current_user)
    review = Review.objects.filter(restaurant_id=menu.rest_id).order_by('?').first()
    app = AppReview.objects.filter(rest_id = menu.rest_id).order_by('?').first()
    context = {'menu': menu, 'app': app, 'form': form, 'review': review}
    return render(request, 'bootrc/recom_menu_test.html', context)


# 도보 분당 63m
def recom_menu(cate_list, user):
    i = 0
    probaility = 0.0
    # now = strftime("%H:%M", gmtime())
    menu_list = RestMenu.objects.order_by('?')
    while True:
        probability = 0.0  # 최종 메뉴 선별 확률( 마지막에 종합된 숫자로 확률 돌림 )
        rest_star = menu_list[i].rest.rest_star
        rest_cate = Categories.objects.filter(rest_id=menu_list[i].rest.rest_num)
        """
        # 가게 운영시간 기준에 맞지 않으면 다시 불러오기
        if time + datetime.timedelta(minutes=(menu_list[i].rest.rest_distance_fromBD/63)+60)
        < menu_list[i].closing_time or 
        time + datetime.timedelta(minutes=(menu_list[i].rest.rest_distance_fromBD/63))
        < menu_list[i].opening_time:
            i += 1
            continue
        """
        # 도보(기본값)일 경우 가게와 떨어진 거리가 300이하인 경우 확률에 +5%
        if set(cate_list) != set(rest_cate):
            i += 1
            continue
        elif menu_list[i].rest.rest_distance_fromBD > 1000:
            i += 1
            continue
        elif menu_list[i].rest.rest_distance_fromBD < 300:
            probaility += 5
        # 별점 기준 확률 조정( 낮을 수록 적은 확률 )
        probability += (rest_star ** 2) * 2
        result = random.randrange(0, 100)

        if result <= probability:
            return menu_list[i]
        else:
            i += 1
        if i == len(menu_list):
            i = 0


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
            rest_list = Rest.objects.order_by('rest_num')
            if rest_list:
                for rest in rest_list:
                    rest.distance_calc()
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

@login_required(login_url='bootrc:login')
def menu_favorite(request):  # 음식 선호도 조사
    random_menu = RestMenu.objects.order_by('?').first() # 랜덤 메뉴 하나
    current_user = request.user
    if request.method == "POST":
        form = PreferForm(request.POST)
        if form.is_valid():
            prefer = form.save(commit=False)
            prefer.user_num = current_user
            prefer.save()

            form = PreferForm()
            context = {'random_menu': random_menu, 'current_user': current_user, 'form': form}
            return render(request, 'bootrc/menu_list_favorite_select.html', context)
    else:
        form = PreferForm()
    context = {'random_menu': random_menu, 'current_user': current_user, 'form': form}
    return render(request, 'bootrc/menu_list_favorite_select.html', context)


def menu_delete(request, menu_menu_num):
    '''
    질문삭제
    '''
    menu = get_object_or_404(Menu, pk=menu_menu_num)
    menu.delete()
    return redirect('bootrc:menu_list')

def crawling_delete(request):
    '''
    크롤링 데이터 (가게, 메뉴, 리뷰) 삭제
    '''
    Review.objects.all().delete()
    RestMenu.objects.all().delete()
    Rest.objects.all().delete()

    return redirect('bootrc:index')

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

def admin_tools(request):
    return render(request, 'bootrc/admin.html')

def app_review(request):
    if request.method == 'POST':
        form = AppReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('bootrc:index')
    else:
        form = AppReviewForm()
    current_user = request.user
    recommend = recentRecommended.objects.filter(user_id=current_user).order_by('-id').first()
    #menu = recom_menu()
    #nowtime = datetime.now().strftime('%H:%M')
    context = {'recommend': recommend, 'form': form}
    return render(request, 'bootrc/app_review.html', context)

def category_select(request):
    if request.method == 'POST':
        selected = request.POST.getlist('selected')
        for obj in selected:
            PreferCate.objects.create(
                user_num=request.user,
                category=obj
            )
        return redirect('bootrc:index')
    else:
       category = Categories.objects.all().order_by('-name')
       category_name = category.values_list('name', flat=True).distinct()
       current_user = request.user
       cate_list = PreferCate.objects.filter(user_num=current_user).order_by('-id')
       context = {'category_name': category_name, 'cate_list': cate_list}
       return render(request, 'bootrc/category_select.html', context)

