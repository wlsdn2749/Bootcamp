from django.urls import path
from . import views

app_name = 'bootrc'

urlpatterns = [
    path('login/', views.login, name='login'),  # 회원(또는 가입용) 페이지로 이동
    path('bootrc/', views.index, name='index'),
    path('menu/list/', views.menu_list, name='menu_list'),
    path('rest/list/', views.rest_list, name='rest_list'),
    path('menu/create/', views.menu_create, name='menu_create'),
    path('rest/create/', views.rest_create, name='rest_create'),
    path('restmenu/list/<int:rest_rest_num>', views.restmenu_list, name='restmenu_list'),
    path('restmenu/create/<int:rest_rest_num>', views.restmenu_create, name='restmenu_create'),
    path('main/', views.main, name='main'),  # 메인 링크에서는 회원, 비회원 구분하는 페이지
]
