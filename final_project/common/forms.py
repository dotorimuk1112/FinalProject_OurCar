from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    phone_number = forms.CharField(label="전화번호")  # 전화번호 필드 추가
    real_name = forms.CharField(max_length=100)  # 예시로 최대 길이 100으로 설정했습니다.
    class Meta:
        model = CustomUser  
        fields = ("real_name", "username", "password1", "password2", "email", "phone_number")
