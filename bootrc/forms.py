from django import forms
from .models import Menu, Rest, RestMenu


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu  # 사용할 모델
        fields = ['menu_catenum', 'menu_name2']  # MenuForm 에서 사용할 Menu모델의 2가지 속성

class RestForm(forms.ModelForm):
    class Meta:
        model = Rest  # 사용할 모델
        fields = ['rest_name', 'rest_star']  # RestForm에서 사용할 rest모델의 1가지 속성


class RestMenuForm(forms.ModelForm):
    class Meta:
        model = RestMenu  # 사용할 모델
        fields = ['rest_menu']  # RestForm에서 사용할 rest모델의 1가지 속성