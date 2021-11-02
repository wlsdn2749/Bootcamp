# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Menu(models.Model):
    menu_num = models.AutoField(primary_key=True) # 메뉴번호 (primary : autofield 자동증가 )
    menu_catenum = models.IntegerField() #메뉴 카테고리 번호
    menu_name2 = models.CharField(max_length=30) #메뉴 이름

class Prefer(models.Model):
    user_num = models.IntegerField() #유저이름 (foreign key)
    pref_menu = models.IntegerField() # 선호하는 메뉴 (foreign ? )
    pref_mod = models.IntegerField() # 선호하는지 안하는지 0 : 선호 1: 비선호

class Rest(models.Model):
    rest_num = models.AutoField(primary_key=True) # 가게 고유번호 (primary : autofield)
    rest_name = models.CharField(max_length=30) #  가게 이름
    rest_star = models.FloatField(default=5)

class RestMenu(models.Model):
    rest = models.ForeignKey(Rest, on_delete=models.CASCADE) #가게를 나타내는 foreignkey
    rest_menu = models.CharField(max_length=30)  # 가게 메뉴

#아직 안만듬
class User(models.Model):
    user_num = models.AutoField(primary_key=True)
    id = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    nickname = models.CharField(max_length=10)
    email = models.CharField(max_length=100)

