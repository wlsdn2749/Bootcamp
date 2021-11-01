from django.urls import path
from . import views

app_name = 'bootrc'

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/list/', views.menu_list, name='menu_list'),
    path('rest/list/', views.rest_list, name='rest_list'),
    path('menu/create/', views.menu_create, name='menu_create'),
    path('rest/create/', views.rest_create, name='rest_create'),
    path('restmenu/list/<int:rest_rest_num>', views.restmenu_list, name='restmenu_list'),
    path('restmenu/create/<int:rest_rest_num>', views.restmenu_create, name='restmenu_list'),
]