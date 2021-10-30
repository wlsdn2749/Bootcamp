# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Menu(models.Model):
    menu_num = models.AutoField(primary_key=True)
    menu_catenum = models.IntegerField()
    menu_name2 = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'menu'


class Prefer(models.Model):
    user_num = models.IntegerField()
    pref_menu = models.IntegerField()
    pref_mod = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'prefer'


class Rest(models.Model):
    rest_num = models.AutoField(primary_key=True)
    rest_name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'rest'


class RestMenu(models.Model):
    rest_num = models.IntegerField()
    rest_menu = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rest_menu'


class User(models.Model):
    user_num = models.AutoField(primary_key=True)
    id = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    nickname = models.CharField(max_length=10)
    email = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'user'
