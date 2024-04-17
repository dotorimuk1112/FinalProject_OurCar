# pybo/views/base_views.py

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Question
from common.models import TestSangmin
from ..forms import ProfileImageForm
import pickle
import pandas as pd

with open('budget_recommend_models.pkl', 'rb') as f:
    budget_rec_model = pickle.load(f)

# 메인 질문 리스트 + 페이지네이션
def index(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    
    paginator = Paginator(question_list, 12)  # 페이지당 12개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'pybo/question_list.html', context)

# 질문 상세 보기
def detail(request, question_id):
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def my_page(request):
    user = request.user
    
    if request.method == 'POST':
        try:
            test_sangmin_instance = TestSangmin.objects.get(id=user.id)
            data = {
                'INTERIOR_AM': [test_sangmin_instance.interior_am],
                'INSUHOS_AM': [test_sangmin_instance.insuhos_am],
                'OFFEDU_AM': [test_sangmin_instance.offedu_am],
                'TRVLEC_AM': [test_sangmin_instance.trvlec_am],
                'FSBZ_AM': [test_sangmin_instance.fsbz_am],
                'SVCARC_AM': [test_sangmin_instance.svcarc_am],
                'DIST_AM': [test_sangmin_instance.dist_am],
                'PLSANIT_AM': [test_sangmin_instance.plsanit_am],
                'CLOTHGDS_AM': [test_sangmin_instance.clothgds_am]
            }

            data_df = pd.DataFrame(data)
            print(data_df)
            
            if budget_rec_model:
                budget_rec_result = budget_rec_model.predict(data_df)
                print(budget_rec_result)
            else:
                print("budget_rec_model is None")
                budget_rec_result = None
                
        except TestSangmin.DoesNotExist:
            test_sangmin_instance = None
            print('데이터가 존재하지 않습니다.')
        
    liked_questions = Question.objects.filter(voter=user)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(liked_questions, 8)
    page_obj = paginator.get_page(page)
    
    profile_image = user.profile_image
    if request.method == 'POST':
        print("post----------------------")
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user)
        print(request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'pybo/my_page.html', {'liked_questions': page_obj, 'budget_rec_result': budget_rec_result, 'test_sangmin_instance': test_sangmin_instance, 'profile_image': profile_image, 'profile_image_form': form})  # Render the user's profile page
            # return redirect("/")  # Render the user's profile page
    else:
        form = ProfileImageForm(instance=request.user)
        print("get----------------------")

    return render(request, 'pybo/my_page.html', {'liked_questions': page_obj, 'budget_rec_result': budget_rec_result, 'test_sangmin_instance': test_sangmin_instance, 'profile_image': profile_image, 'profile_image_form': form})
    
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