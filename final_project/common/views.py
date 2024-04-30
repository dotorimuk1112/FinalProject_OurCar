from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from common.forms import CustomUserForm  # CustomUserForm을 사용하기 위해 import
from django.contrib import messages
from .models import CarAPI, CustomUser
from sales.models import CarSalesPost
from django.http import HttpResponse
from .forms import CustomPasswordChangeForm,CustomUserUpdateForm
from django.contrib.auth import update_session_auth_hash
from common.static.car_price_pred import car_price_pred_model, car_price_pred_model_10000

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
            # login(request, user)
            return redirect('index')
    else:
        form = CustomUserForm()  # CustomUserForm 사용
    return render(request, 'common/signup.html', {'form': form})

def car_info(request):
    error_message = None
    car = None
    mae = None
    predicted_price = None
    predicted_list = []
    mae_10000 = None
    min_price = None
    max_price = None
    already_registered = None
    if request.method == 'POST':
        car_number = request.POST.get('car_number')
        car = CarAPI.objects.get(VNUM=car_number)
        predicted_price, mae = car_price_pred_model(car)
        predicted_list, mae_10000 = car_price_pred_model_10000(car)
        
        if mae:
            min_price = int(predicted_price - float(mae))
            max_price = int(predicted_price + float(mae))
            already_registered = CarSalesPost.objects.filter(VNUM=car_number).first()
        else:
            min_price = None
            max_price = None
            already_registered = CarSalesPost.objects.filter(VNUM=car_number).first()
    return render(request, 'common/car_info.html', {'car': car, 'min_price': min_price, 'max_price': max_price, 'error_message': error_message, 'predicted_list': predicted_list, 'mae_10000': mae_10000, 'already_registered':already_registered})


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
