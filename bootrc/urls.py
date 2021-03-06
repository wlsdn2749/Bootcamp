from django.urls import path
from . import views
from django.contrib.auth import views as auth_views #django의 자체 로그인 기능 사용
from . import models
from django.conf import settings
from django.conf.urls.static import static

app_name = 'bootrc'

urlpatterns = [
    path('login',auth_views.LoginView.as_view(template_name='bootrc/login.html'),name='login'), # 로그인 페이지로 이동
    path('logout',auth_views.LogoutView.as_view(),name='logout'), # 로그아웃 기능
    path('signup',views.signup,name='signup'), # 회원가입 페이지로 이동
    path('', views.index, name='index'),
    path('menu/list/', views.menu_list, name='menu_list'),
    path('rest/list/', views.rest_list, name='rest_list'),
    path('menu/create/', views.menu_create, name='menu_create'),
    path('rest/create/', views.rest_create, name='rest_create'),
    path('restmenu/list/<int:rest_rest_num>', views.restmenu_list, name='restmenu_list'),
    path('restmenu/create/<int:rest_rest_num>', views.restmenu_create, name='restmenu_create'),
    path('main/', views.main, name='main'),  # 메인 링크에서는 회원, 비회원 구분하는 페이지
    path('menu/delete/<int:menu_menu_num>', views.menu_delete, name='menu_delete'),
    path('rest/delete/<int:rest_rest_num>', views.rest_delete, name='rest_delete'),
    path('crawling', views.crawling, name='crawling'),
    path('crawling_delete', views.crawling_delete, name='crawling_delete'),
    path('recommendmenu', views.recommendmenu, name='recommendmenu'),
    path('restmenu/delete/<int:restmenu_id>', views.restmenu_delete, name='restmenu_delete'),
    path('menufavorite/', views.menu_favorite, name='menu_select'),
    path('tools',views.admin_tools,name='admin_tools'),
    path('recom_menu_test/', views.recommendmenu2, name='recommendmenu2'),
    path('app_review/', views.app_review, name='app_review'),
    path('category_select/', views.category_select, name='category_select'),
    path('rest_ranking/', views.rest_ranking, name='rest_ranking'),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
