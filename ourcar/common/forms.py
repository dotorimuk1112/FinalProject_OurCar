from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    phone_number = forms.CharField(label="전화번호")  # 전화번호 필드 추가

    class Meta:
        model = CustomUser  
        fields = ("username", "password1", "password2", "email", "phone_number")
