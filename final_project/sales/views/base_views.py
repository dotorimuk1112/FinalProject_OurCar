# pybo/views/base_views.py

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import CarSalesPost
from common.models import TestSangmin
from ..forms import ProfileImageForm
import pickle
import pandas as pd
import numpy as np

with open('budget_recommend_models.pkl', 'rb') as f:
    budget_rec_model = pickle.load(f)

# 메인 질문 리스트 + 페이지네이션
def index(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    brand_filter = request.GET.get('brand', '')  # 브랜드 필터
    
    car_list = CarSalesPost.objects.order_by('-create_date')
    
    if kw:
        car_list = car_list.filter(
            Q(MNAME__icontains=kw)   # 제목 검색
        ).distinct()
    
    if brand_filter:
        car_list = car_list.filter(
            Q(MNAME__icontains=brand_filter)  # 제목에 브랜드명이 포함된 차량 필터링
        ).distinct()
    
    paginator = Paginator(car_list, 12)  # 페이지당 12개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'car_list': page_obj, 'page': page, 'kw': kw, 'brand_filter': brand_filter}
    return render(request, 'sales/question_list.html', context)

# 질문 상세 보기
def detail(request, post_id):
    car_sales_post = get_object_or_404(CarSalesPost, post_id=post_id)
    context = {'CarSalesPost': car_sales_post}
    return render(request, 'sales/sales_detail.html', context)

@login_required(login_url='common:login')
def my_page(request):
    user = request.user
    test_sangmin_instance = None

    try:
        test_sangmin_instance = TestSangmin.objects.get(id=user.id)
        data = {
            'INTERIOR_AM': [int(test_sangmin_instance.interior_am)],
            'INSUHOS_AM': [int(test_sangmin_instance.insuhos_am)],
            'OFFEDU_AM': [int(test_sangmin_instance.offedu_am)],
            'TRVLEC_AM': [int(test_sangmin_instance.trvlec_am)],
            'FSBZ_AM': [int(test_sangmin_instance.fsbz_am)],
            'SVCARC_AM': [int(test_sangmin_instance.svcarc_am)],
            'DIST_AM': [int(test_sangmin_instance.dist_am)],
            'PLSANIT_AM': [int(test_sangmin_instance.plsanit_am)],
            'CLOTHGDS_AM': [int(test_sangmin_instance.clothgds_am)]
        }

        data_df = pd.DataFrame(data)
        print(data_df)
        
        if budget_rec_model:
            budget_rec_result = budget_rec_model.predict(data_df)
            budget_rec_result = np.squeeze(budget_rec_result)
            budget_rec_result = int(budget_rec_result)
            min_budget = budget_rec_result - 147
            max_budget = budget_rec_result + 147
            print("예측 결과:", "최소 예산-", min_budget, "|", "최대 예산-", max_budget)
        else:
            print("budget_rec_model is None")
            budget_rec_result = None
            
    except TestSangmin.DoesNotExist:
        test_sangmin_instance = None
        print('데이터가 존재하지 않습니다.')
        
    # 사용자가 좋아하는 차량 가져오기
    liked_car = CarSalesPost.objects.filter(buyer=user)
    
    # 사용자가 판매한 차량 가져오기
    user_cars_for_sale = CarSalesPost.objects.filter(seller=user)
    
    # 페이지네이션 추가
    liked_car_page = request.GET.get('liked_car_page', 1)  # 좋아하는 차량 페이지 번호
    user_cars_for_sale_page = request.GET.get('user_cars_for_sale_page', 1)  # 판매 중인 차량 페이지 번호
    
    liked_car_paginator = Paginator(liked_car, 8)  # 좋아하는 차량 페이지당 8개씩 보여주기
    user_cars_for_sale_paginator = Paginator(user_cars_for_sale, 8)  # 판매 중인 차량 페이지당 8개씩 보여주기
    
    liked_car_page_obj = liked_car_paginator.get_page(liked_car_page)
    user_cars_for_sale_page_obj = user_cars_for_sale_paginator.get_page(user_cars_for_sale_page)
    
    # 좋아하는 차량과 판매 중인 차량의 개수
    liked_car_count = liked_car.count()
    user_cars_for_sale_count = user_cars_for_sale.count()
    
    # 사용자의 프로필 이미지를 가져옵니다.
    profile_image = user.profile_image
    
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, 'sales/my_page.html', {
                'liked_car': liked_car_page_obj,
                'user_cars_for_sale': user_cars_for_sale_page_obj,
                'budget_rec_result': budget_rec_result,
                'test_sangmin_instance': test_sangmin_instance,
                'profile_image': profile_image,
                'profile_image_form': form,
                'liked_car_count': liked_car_count,
                'user_cars_for_sale_count': user_cars_for_sale_count
            })  
    else:
        form = ProfileImageForm(instance=request.user)

    return render(request, 'sales/my_page.html', {
        'liked_car': liked_car_page_obj,
        'user_cars_for_sale': user_cars_for_sale_page_obj,
        'min_budget': min_budget,
        'max_budget': max_budget,
        'test_sangmin_instance': test_sangmin_instance,
        'profile_image': profile_image,
        'profile_image_form': form,
        'liked_car_count': liked_car_count,
        'user_cars_for_sale_count': user_cars_for_sale_count
    })


# @login_required(login_url='common:login')
# def upload_profile_image(request):
#     if request.method == 'POST':
#         form = ProfileImageForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return render(request, 'my_page')  # Render the user's profile page
#     else:
#         form = ProfileImageForm(instance=request.user)
#     return render(request, 'pybo/upload_profile_image.html', {'profile_image_form': form})