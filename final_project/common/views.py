from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from common.forms import CustomUserForm  # CustomUserForm을 사용하기 위해 import
from .models import Car
import pickle
import pandas as pd
from django.http import HttpResponse


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
            predicted_price = loaded_model.predict(data_df)
            return render(request, 'common/car_info.html', {'car': car, 'predicted_price': predicted_price})
        except Car.DoesNotExist:
            error_message = "해당하는 차량 정보가 없습니다."
            return render(request, 'common/car_info.html', {'error_message': error_message})
    return render(request, 'common/car_info.html')