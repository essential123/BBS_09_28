from django import forms

from .models import User
from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=8, min_length=3, required=True, label='用户名',
                               widget=widgets.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=8, min_length=3, required=True, label='密码',
                               widget=widgets.PasswordInput(attrs={'class': 'form-control'}))
    re_password = forms.CharField(max_length=8, min_length=3, required=True, label='确认密码',
                                  widget=widgets.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='邮箱', widget=widgets.EmailInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            raise ValidationError('该用户已存在')
        else:
            return username

    def clean(self):
        # cleaned_data {}
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password == re_password:
            return self.cleaned_data
        else:
            raise ValidationError('两次密码不一致')
