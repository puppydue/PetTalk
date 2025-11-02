from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Tên người dùng',
        'class': 'input-field',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Mật khẩu',
        'class': 'input-field',
    }))

class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'input-field',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Tên người dùng',
        'class': 'input-field',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Mật khẩu',
        'class': 'input-field',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Nhập lại mật khẩu',
        'class': 'input-field',
    }))
