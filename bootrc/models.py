# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from math import *
from haversine import haversine  # haversine 은 위도 경도로 거리 계산 함수
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Menu(models.Model):
    menu_num = models.AutoField(primary_key=True)  # 메뉴번호 (primary : autofield 자동증가 )
    menu_catenum = models.IntegerField()  # 메뉴 카테고리 번호
    menu_name2 = models.CharField(max_length=30)  # 메뉴 이름


class Prefer(models.Model):
    user_num = models.ForeignKey(User, on_delete=models.CASCADE)  # 유저이름 (foreign key)
    pref_menu = models.ForeignKey('RestMenu', on_delete=models.CASCADE)  # 선호하는 메뉴 (foreign ? )
    pref_like = models.IntegerField()  # 선호하는지 안하는지 0 ~ +

class PreferCate(models.Model):
    user_num = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(default = '', max_length=30)

class Rest(models.Model):
    rest_num = models.AutoField(primary_key=True)  # 가게 고유번호 (primary : autofield)
    rest_name = models.CharField(max_length=30)  # 가게 이름
    rest_star = models.FloatField(default=5)
    rest_location_lat = models.FloatField(default=0)  # 가게 위도
    rest_location_lon = models.FloatField(default=0)  # 가게 경도
    rest_recent_user = models.IntegerField(default=0)  # 이용자 수
    rest_number_reviews = models.IntegerField(default=0)  # 리뷰 개수
    rest_distance_fromBD = models.IntegerField(default=0)  # 후문에서 가게 거리
    opening_time = models.TimeField(default='00:00')
    closing_time = models.TimeField(default='00:00')
    phone_number = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=255, default='')
    yogiyo_id = models.IntegerField(default=0)

    image = models.ImageField(upload_to='restaurant_image', null=True, blank=True)
    back_image = models.ImageField(upload_to='restaurant_back_image', null=True, blank=True)


    def distance_calc(self):
        school_bd = (35.817094, 127.090152)     # 학교 후문의 위도 경도
        destination = (self.rest_location_lat, self.rest_location_lon)  # 목적지 위도 경도
        distance = haversine(school_bd, destination, unit='m')
        result = int(distance)
        # haversine 은 위도 경도로 거리 계산 함수 from haversine, unit 은 거리 표현 방법
        self.rest_distance_fromBD = result
        self.save()
        return result


def menu_img_path(instance, filename):
    filename = filename.split('?')[0]
    return f'menu_img/{filename}'

class RestMenu(models.Model):
    rest = models.ForeignKey(Rest, on_delete=models.CASCADE)  # 가게를 나타내는 foreignkey
    rest_menu = models.CharField(max_length=30)  # 가게 메뉴
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='menu_image', null=True, blank=True, max_length=400)
    recommendmenu = models.FloatField(default=0)

    def recommend_calc(self):
        result = (
            self.rest.rest_star * 2 +# 별점 가중치 25%
            (1000 - self.rest.rest_distance_fromBD) / 100 +  # 거리 가중치 25%
            self.rest.rest_recent_user / 100 + # 이용자 수 가중치 25%
            self.rest.rest_number_reviews / 100 # 리뷰 개수 가중치 25%
            # + 유저의 좋거나 싫거나 하는?
        )
        self.recommendmenu = result
        self.save()

class Review(models.Model):
    restaurant = models.ForeignKey('Rest', on_delete=models.CASCADE, related_name='review') # 리뷰의 가게 foreginkey
    comment = models.CharField(max_length=300) # 리뷰내용
    rating = models.PositiveIntegerField(default=0)#(vaildators=[MinValueValidator(0), MaxValueValidator(5)]) # 리뷰의 별점
    menu_name = models.CharField(max_length=100) # 리뷰한 메뉴이름
    created = models.DateTimeField(auto_now_add=True) # 작성일이 언제인지
    like_count = models.PositiveIntegerField(default=0) #리뷰의 좋아요 갯수

    class Meta:
        ordering = ['-id']


class Categories(models.Model):
    name = models.CharField(max_length=300)
    rest = models.ForeignKey('Rest',on_delete=models.CASCADE, related_name='categories')

class recentRecommended(models.Model):
    rest = models.ForeignKey('Rest',on_delete=models.CASCADE, related_name='recent_recommended') # 최근 추천된 가게
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 유저
    menu_name = models.ForeignKey('RestMenu', on_delete=models.CASCADE) # 최근 추천된 메뉴이름
    comment = models.CharField(max_length=300, default='') # 리뷰 내용
    like_count = models.PositiveIntegerField(default=0)  #리뷰의 좋아요 갯수
    created = models.DateTimeField(auto_now_add=True)  # 추천 된 날짜가 언제인지

    class Meta:
        ordering = ['-id']

class AppReview(models.Model):
    rest = models.ForeignKey('Rest',on_delete=models.CASCADE, related_name='app_review') # 최근 추천된 가게
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 유저
    menu_name = models.ForeignKey('RestMenu', on_delete=models.CASCADE) # 최근 추천된 메뉴이름
    comment = models.CharField(max_length=300, default='') # 리뷰 내용
    like_count = models.PositiveIntegerField(default=0)  #리뷰의 좋아요 갯수
    created = models.DateTimeField(auto_now_add=True)  # 추천 된 날짜가 언제인지