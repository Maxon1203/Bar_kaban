import re
from django.core.exceptions import ValidationError

from django import forms
from .models import *

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User



class BarSearchForm(forms.Form):
    search_query = forms.CharField(label='Поиск по названию бара', max_length=100)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
        min_length=2
    )
    email = forms.CharField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-control', }),
    )
    password1 = forms.CharField(
        label='Придумайте пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )
    avatar = forms.ImageField(
        label='Выберите фото'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'avatar']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
        min_length=2
    )
    password = forms.CharField(
        label='Ваш пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )

class UserEditForm(forms.ModelForm):
    avatar = forms.ImageField(
        label='Выберите фото'
    )
    password = forms.CharField(widget=forms.TextInput(attrs={'type': 'password'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'avatar']
