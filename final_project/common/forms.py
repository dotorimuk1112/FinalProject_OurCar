from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    phone_number = forms.CharField(label="전화번호")  
    real_name = forms.CharField(max_length=100)  
    address = forms.CharField(label="주소", max_length=255, required=False)  # address 필드 추가
    gender = forms.ChoiceField(label="성별", choices=CustomUser.GenderChoices.choices, required=False)
    
    class Meta:
        model = CustomUser  
        fields = ("real_name", "username", "password1", "password2", "email", "phone_number", "gender", "address")
