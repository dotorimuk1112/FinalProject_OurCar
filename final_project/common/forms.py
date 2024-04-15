from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
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

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = '기존 비밀번호'
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': False,
        })
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
        })
        
class CustomUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="이메일")
    phone_number = forms.CharField(label="전화번호")
    address = forms.CharField(label="주소", max_length=255, required=False)
    gender = forms.ChoiceField(label="성별", choices=CustomUser.GenderChoices.choices, required=False)

    class Meta:
        model = CustomUser
        fields = ("email", "phone_number", "gender", "address")
