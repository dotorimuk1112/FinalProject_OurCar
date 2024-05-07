# pybo/views/base_views.py

from django.core.paginator import Paginator
from django.core import serializers
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import CarSalesPost, BuyerMessages
from common.models import predict_budget, CustomUser, CarAPI
from ..forms import ProfileImageForm
import pickle
import seul_car_list
from django.db.models import Count
from ..static.budget_rec import budget_rec_func
from django.http import HttpResponse
from django.contrib import messages
from common.static.car_price_pred import car_price_pred_model, car_price_pred_model_10000, car_price_pred_model_20000, car_price_pred_model_30000
from sales.static.card_scoring import scoring_data
from common.models import loan_rate_list
import math

# with open('/app/final_project/ai_models/budget_recommend_models.pkl', 'rb') as f:
with open('ai_models/budget_recommend_models.pkl', 'rb') as f:
    budget_rec_model = pickle.load(f)


# 메인 질문 리스트 + 페이지네이션
def index(request):
    user = request.user
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    sorting_option = request.GET.get('sorting_option', 'date')  # 기본값은 'date'
    sorting_region = request.GET.get('sorting_region', '서울')
    budget_filter = request.GET.get('budget_option', '-1')
    personal_page = request.GET.get('personal_page', False)
    mile_mode = request.GET.get('mile_mode') 
    vtype_mode = request.GET.get('vtype_mode') 
    # CarSalesPost 모델의 MYERAR 필드 값들을 중복 제거하여 리스트로 가져오기
    myerar_values = CarSalesPost.objects.values_list('MYERAR', flat=True).order_by('-MYERAR').distinct()
    myerar_values = [str(value) for value in myerar_values]

    vtype_values = list(sorted(CarSalesPost.objects.values_list('VTYPE', flat=True).distinct()))
    
    # 중복 제거된 MYERAR 필드 값들을 리스트로 변환
    myerar_list = list(myerar_values)

    # 선택한 정렬 옵션에 따라 정렬 적용
    if sorting_option == 'date':
        car_list = CarSalesPost.objects.order_by('-create_date')
    elif sorting_option == 'popularity':
        car_list =  CarSalesPost.objects.annotate(num_buyers=Count('buyer')).order_by('-num_buyers')
    elif sorting_option == "lowprice":
        car_list = CarSalesPost.objects.order_by('PRICE')
    elif sorting_option == "highprice":
        car_list = CarSalesPost.objects.order_by('-PRICE')
    elif sorting_option == 'region':
        if sorting_region:
            if sorting_region != "전체":
                car_list = CarSalesPost.objects.filter(
                    Q(seller__address__icontains=sorting_region)
                ).distinct()
            

        
        

    # 다른 필터링 로직은 동일하게 유지
    
    
    ko_brands = seul_car_list.ko_brand

    if kw:
        car_list = car_list.filter(
            Q(MNAME__icontains=kw)   # 제목 검색
        ).distinct()

    search_mode = request.GET.get('search_mode')
    search_mode2 = request.GET.get('search_mode2')

    print(search_mode)
    if search_mode:
        if search_mode != "전체":
            car_list = car_list.filter(
                Q(MNAME__icontains=search_mode)
            ).distinct()
        
        # search_mode에 해당하는 키에 맞는 value 가져오기
        selected_brand_values = ko_brands.get(search_mode, [])
    else:
        selected_brand_values = []

    if search_mode2:
        if search_mode2 != "전체":
            car_list = car_list.filter(
                Q(MNAME__icontains=search_mode2)
            ).distinct()
        print("세부 차종명 :" + str(len(selected_brand_values)))
        
    # 연식 필터   
    if mile_mode :
        car_list = car_list.filter(MYERAR=mile_mode)
        
    # 차종(크기) 필터   
    if vtype_mode :
        car_list = car_list.filter(VTYPE=vtype_mode)
    # 예산 추천
    min_budget, max_budget, budget_rec_result = budget_rec_func(user.id)
    
    
    if personal_page :
        car_list = car_list.filter(PRICE__gte=min_budget, PRICE__lte=max_budget)
    else :
        car_list =car_list.filter(PRICE__lt=10000000000)
        
    if budget_filter == '-1' :
        car_list =car_list.filter(PRICE__lt=10000000000)
    else : 
        # car_list에서 PRICE 가격이 higher_budget보다 작은 게시글 필터링
        car_list = car_list.filter(PRICE__gte=min_budget, PRICE__lte=max_budget) 
        min_price = min_budget
        max_price = max_budget   
    
    if car_list :
        myerar_values  = car_list.filter(MYERAR__in=myerar_values)
    
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    ## 주행거리 
    min_mileage = request.GET.get('min_mileage')
    max_mileage = request.GET.get('max_mileage')
    
    
    if min_price:
        car_list = car_list.filter(PRICE__gte=min_price)

    if max_price:
        car_list = car_list.filter(PRICE__lte=max_price)

    
    if min_mileage:
        car_list = car_list.filter(MILEAGE__gte=min_mileage)

    if max_mileage:
        car_list = car_list.filter(MILEAGE__lte=max_mileage)

    paginator = Paginator(car_list, 12)  # 페이지당 12개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'car_list': page_obj, 'page': page, 
               'kw': kw, 'ko_brands' : ko_brands, 
               'selected_brand_values': selected_brand_values, 
               'search_mode' :search_mode, 'search_mode2' :search_mode2, 
               'sorting_option' : sorting_option, 
               'sorting_region':sorting_region,
               'budget_filter': budget_filter,
               'personal_page':personal_page,
               'myerar_list': myerar_list, 
               'mile_mode' : mile_mode,
               'vtype_values' : vtype_values,
               'vtype_mode' : vtype_mode,
               'min_budget':min_budget,
               'max_budget': max_budget}
    return render(request, 'sales/question_list.html', context)

# 질문 상세 보기
from django.shortcuts import get_object_or_404


def accept_proposal(request, proposal_id):
    if request.method == 'POST':
        proposal = get_object_or_404(BuyerMessages, id=proposal_id)
        accepted_value = request.POST.get('accepted')
        if accepted_value == 'True':
            proposal.accepted = True
        elif accepted_value == 'False':
            proposal.accepted = False
        proposal.save()
        # 성공 메시지 추가
        messages.success(request, '성공적으로 전달되었습니다.')
        return redirect('sales:detail', post_id=proposal.post_id)
    else:
        return HttpResponse('잘못된 요청입니다.')

# 가격 제시 레코드 삭제
def cancel_proposal(request, post_id):
    # 현재 접속한 사용자와 해당 게시글(post_id)에 해당하는 구매 제안서 가져오기
    proposal = get_object_or_404(BuyerMessages, buyer=request.user, post_id=post_id)

    # 구매 제안서를 삭제
    proposal.delete()

    # 삭제 후 리다이렉트
    return redirect('sales:detail', post_id)

# 대출 상품 데이터 가져오기
def load_loans(term, score):
    score_00 = math.floor(score/100)*100
    list_filtered_credit = loan_rate_list.objects.filter(credit_range=score_00)
    list_filtered = list_filtered_credit.filter(loan_period=term)
    list_ordered = list_filtered.order_by('min_rate')[:5]
    woori_loan = list_filtered_credit.get(company_name="우리은행")
    return list_ordered, woori_loan

# 대출 상품 데이터 전송
def show_loan_table(request, post_id):
    user = request.user
    input_term = request.GET.get('term')
    user_credit_score = scoring_data(user_id=user.id)
    loans, woori_loan = load_loans(input_term, user_credit_score)
    loan_list = serializers.serialize('json', loans)
    return HttpResponse(loan_list, content_type="text/json-comment-filtered")

# 질문 상세 보기
def detail(request, post_id):
    user = request.user
    car_sales_post = get_object_or_404(CarSalesPost, post_id=post_id)
    vnum_value = car_sales_post.VNUM
    car = CarAPI.objects.get(VNUM=vnum_value)
    predicted_price, mae = car_price_pred_model(car)

    min_price = None
    max_price = None
    predicted_list_10000, mae_10000 = None, None
    predicted_list_20000, mae_20000 = None, None
    predicted_list_30000, mae_30000 = None, None

    if predicted_price and mae:
        min_price = int(predicted_price - float(mae))
        max_price = int(predicted_price + float(mae))
        predicted_list_10000, mae_10000 = car_price_pred_model_10000(car)
        predicted_list_20000, mae_20000 = car_price_pred_model_20000(car)
        predicted_list_30000, mae_30000 = car_price_pred_model_30000(car)

    average_mileage = int(car.MILEAGE / (2024 - car.MYERAR + 1))
    min_budget, max_budget, budget_rec_result = 0, 0, 0

    if user:
        min_budget, max_budget, budget_rec_result = budget_rec_func(user.id)
    
    # 해당 게시글에 대한 구매 제안서 목록을 가져오기
    buyer_proposals = BuyerMessages.objects.filter(post_id=post_id)
    buyer_list = [proposal.buyer_id for proposal in buyer_proposals]    # 해당 게시글에 대한 구매 제안서 목록을 가져오기
    # 구매 제안서 목록을 반복하면서 구매자 정보와 함께 가져오기
    buyer_proposals_with_info = []
    for proposal in buyer_proposals:
        # 각 구매 제안서의 구매자 정보를 가져오기
        buyer_info = get_object_or_404(CustomUser, id=proposal.buyer_id)
        # 구매 제안서와 구매자 정보를 함께 저장
        buyer_proposals_with_info.append((proposal, buyer_info))
    
    # 사용자에게 맞는 대출 상품 목록 가져오기
    user_credit_score, loan_list, woori_loan = 0, 0, 0
    if user.is_authenticated:
        user_credit_score = scoring_data(user_id=user.id)
        loan_list, woori_loan = load_loans(36, user_credit_score)

    context = {
        'user': user,
        'CarSalesPost': car_sales_post,
        'min_budget': min_budget,
        'max_budget': max_budget,
        'budget_rec_result': budget_rec_result,
        'buyer_proposals_with_info': buyer_proposals_with_info,  # 구매 제안서와 해당 구매자의 정보를 context에 추가
        'min_price': min_price,
        'max_price': max_price,
        'predicted_list_10000': predicted_list_10000,
        'mae_10000': mae_10000,
        'predicted_list_20000': predicted_list_20000,
        'mae_20000': mae_20000,
        'predicted_list_30000': predicted_list_30000,
        'mae_30000': mae_30000,
        'car': car,
        'average_mileage': average_mileage,
        'buyer_list' : buyer_list,
        'loan_list' : loan_list,
        'woori_loan' : woori_loan,
        'user_credit_score' : user_credit_score
    }
    return render(request, 'sales/sales_detail.html', context)



@login_required(login_url='common:login')
def my_page(request):
    user = request.user
    test_sangmin_instance = predict_budget.objects.get(id=user.id)
    
    min_budget, max_budget, budget_rec_result = budget_rec_func(user.id)
        
    # 사용자가 구매 의사 보낸 차량 가져오기
    liked_car = CarSalesPost.objects.filter(buyer=user)
    
    # 사용자가 판매한 차량 가져오기
    user_cars_for_sale = CarSalesPost.objects.filter(seller=user)
    
    # 사용자가 구매 제안한 차량 가져오기
    # 현재 접속한 사용자의 ID
    user_id = request.user.id

    # 현재 접속한 사용자의 ID에 해당하는 모든 BuyerMessages의 post_id를 가져오기
    user_buyer_messages = BuyerMessages.objects.filter(buyer_id=user_id).values_list('post_id', flat=True)
    user_buyer_price = BuyerMessages.objects.filter(buyer_id=user_id).values_list('buyer_price', flat=True)
    # BuyerMessages에 해당하는 CarSalesPost를 가져오기
    buyer_proposed_cars = CarSalesPost.objects.filter(post_id__in=user_buyer_messages)
    for car in buyer_proposed_cars:
        buyer_message = BuyerMessages.objects.filter(post_id=car.post_id).first()  # 해당 게시글에 대한 첫 번째 BuyerMessages 객체 가져오기
        if buyer_message:
            car.buyer_price = buyer_message.buyer_price  # 해당 게시글의 buyer_price를 가져와서 car 객체에 추가   
            car.accepted = buyer_message.accepted 
    # 페이지네이션 추가
    liked_car_page = request.GET.get('liked_car_page', 1)  # 좋아하는 차량 페이지 번호
    user_cars_for_sale_page = request.GET.get('user_cars_for_sale_page', 1)  # 판매 중인 차량 페이지 번호
    buyer_proposed_cars_page = request.GET.get('buyer_proposed_cars_page',1)
    accepted_count = BuyerMessages.objects.filter(accepted=1, post_id__in=[car.post_id for car in buyer_proposed_cars]).count()

    liked_car_paginator = Paginator(liked_car, 8)  # 좋아하는 차량 페이지당 8개씩 보여주기
    user_cars_for_sale_paginator = Paginator(user_cars_for_sale, 8)  # 판매 중인 차량 페이지당 8개씩 보여주기
    buyer_proposed_cars_paginator = Paginator(buyer_proposed_cars, 8)
    
    liked_car_page_obj = liked_car_paginator.get_page(liked_car_page)
    user_cars_for_sale_page_obj = user_cars_for_sale_paginator.get_page(user_cars_for_sale_page)
    buyer_proposed_cars_page_obj = buyer_proposed_cars_paginator.get_page(buyer_proposed_cars_page)
    
    # 좋아하는 차량과 판매 중인 차량의 개수
    liked_car_count = liked_car.count()
    user_cars_for_sale_count = user_cars_for_sale.count()
    buyer_proposed_cars_count = buyer_proposed_cars.count()

    # 사용자의 프로필 이미지를 가져오기
    profile_image = user.profile_image
    # 사용자의 신용 점수 가져오기
    user_credit_score = scoring_data(user_id=user_id)
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, 'sales/my_page.html', {
                'liked_car': liked_car_page_obj,
                'user_cars_for_sale': user_cars_for_sale_page_obj,
                'buyer_proposed_cars' : buyer_proposed_cars_page_obj,
                'budget_rec_result': budget_rec_result,
                'test_sangmin_instance': test_sangmin_instance,
                'profile_image': profile_image,
                'profile_image_form': form,
                'liked_car_count': liked_car_count,
                'user_cars_for_sale_count': user_cars_for_sale_count,
                'accepted_count':accepted_count
                
            })  
    else:
        form = ProfileImageForm(instance=request.user)

    return render(request, 'sales/my_page.html', {
        'liked_car': liked_car_page_obj,
        'user_cars_for_sale': user_cars_for_sale_page_obj,
        'buyer_proposed_cars' : buyer_proposed_cars_page_obj,
        'min_budget': min_budget,
        'max_budget': max_budget,
        'test_sangmin_instance': test_sangmin_instance,
        'profile_image': profile_image,
        'profile_image_form': form,
        'liked_car_count': liked_car_count,
        'user_cars_for_sale_count': user_cars_for_sale_count,
        'buyer_proposed_cars_count' : buyer_proposed_cars_count,
        'user_credit_score' : user_credit_score,
        'accepted_count':accepted_count


    })


