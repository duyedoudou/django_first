# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from .models import UserProfile,UserInfo

class LoginForm (forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username","email")

    def clean_password2(self):   # 检验两次的密码是否一致
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("密码不匹配。")
        return cd['password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone","birth")


# 新增用户表单
class UserInfoForm(forms.ModelForm):      # 针对UserInfo数据模型的
    class Meta:
        model = UserInfo
        fields = ('school','company','profession','address','aboutme','photo')


class UserForm(forms.ModelForm):          # 进行修改的
    class Meta:
        model = User
        fields = ('email',)


