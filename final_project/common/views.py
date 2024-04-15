from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
    PasswordChangeForm,
)
from django.shortcuts import render, redirect, get_object_or_404
from common.forms import CustomUserForm  # CustomUserForm을 사용하기 위해 import
from django.contrib import messages
from sales.forms import SalesForm
from .models import Car, CustomUser
import pickle
import pandas as pd
from django.http import HttpResponse
from .forms import CustomPasswordChangeForm,CustomUserUpdateForm
from django.contrib.auth import update_session_auth_hash

def index(request):
    return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")

def logout_view(request):
    logout(request)
    return redirect('index')

def signup(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)  # CustomUserForm 사용
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserForm()  # CustomUserForm 사용
    return render(request, 'common/signup.html', {'form': form})

# 저장된 모델 불러오기
with open('large_xgboost_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

def car_info(request):
    error_message = None
    car = None
    predicted_price = None
    
    if request.method == 'POST':
        car_number = request.POST.get('car_number')
        try:
            car = Car.objects.get(VNUM=car_number)
            # 입력된 차량 정보를 기반으로 데이터 구성
            data = {
                'MYERAR': [2024 - car.MYERAR + 1],
                'MILEAGE': [car.MILEAGE],
                'DISP': [car.DISP],         
                'CU_HIS': [car.CU_HIS],
                'MVD_HIS': [car.MVD_HIS],
                'AVD_HIS': [car.AVD_HIS],
                'FD_HIS': [car.FD_HIS],
                'VT_HIS': [car.VT_HIS],
                'US_HIS': [car.US_HIS],
            }
            # 데이터를 적절한 형태로 변환하여 모델에 적용
            data_df = pd.DataFrame(data)
            predicted_price = int(round(float(loaded_model.predict(data_df)), 1))
            
        except Car.DoesNotExist:
            error_message = "해당하는 차량 정보가 없습니다."
    
    return render(request, 'common/car_info.html', {'car': car, 'predicted_price': predicted_price, 'error_message': error_message})


# 회원 정보 수정
@login_required(login_url='common:login')
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '회원 정보가 성공적으로 수정되었습니다.')
            return redirect('sales:my_page')
        else:
            print("nononono")
            messages.error(request, '회원 정보 수정에 실패했습니다. 올바른 값을 입력해주세요.')
    else:
        form = CustomUserUpdateForm(instance=request.user)

    context = {
        'form': form,
    }
    return render(request, 'common/edit_profile.html', context)

# 회원 탈퇴
@login_required(login_url='common:login')
def delete_user(request, user_id):
    current_user = get_object_or_404(CustomUser, pk=user_id)
    if request.user != current_user:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('sales:index')
    current_user.delete()
    return redirect('sales:index')


# 비밀번호 변경
@login_required(login_url='common:login')
def password_update(request):
    if request.method == 'POST':
        password_change_form = CustomPasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
            return redirect('sales:my_page')
    else:
        password_change_form = CustomPasswordChangeForm(request.user)

    return render(request, 'common/password_update.html', {'password_change_form':password_change_form})
