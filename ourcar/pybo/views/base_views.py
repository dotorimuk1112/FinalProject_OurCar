# pybo/views/base_views.py

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Question
from common.models import TestSangmin
from ..forms import ProfileImageForm

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
    
    paginator = Paginator(question_list, 12)  # 페이지당 10개씩 보여주기
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
    
    # 사용자에게 연결된 test_sangmin 객체 가져오기
    try:
        test_sangmin_instance = TestSangmin.objects.get(id=user.id)
    except TestSangmin.DoesNotExist:
        test_sangmin_instance = None
        
    liked_questions = Question.objects.filter(voter=user)
    
    # 페이지네이션 추가
    page = request.GET.get('page', 1)  # 현재 페이지 번호
    paginator = Paginator(liked_questions, 8)  # 페이지당 12개씩 보여주기
    page_obj = paginator.get_page(page)
    
    # 사용자의 프로필 이미지를 가져옵니다.
    profile_image = user.profile_image
    if request.method == 'POST':
        print("post----------------------")
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user)
        print(request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'pybo/my_page.html', {'liked_questions': page_obj, 'test_sangmin_instance': test_sangmin_instance, 'profile_image': profile_image, 'profile_image_form': form})  # Render the user's profile page
            # return redirect("/")  # Render the user's profile page
    else:
        form = ProfileImageForm(instance=request.user)
        print("get----------------------")

    return render(request, 'pybo/my_page.html', {'liked_questions': page_obj, 'test_sangmin_instance': test_sangmin_instance, 'profile_image': profile_image, 'profile_image_form': form})
    
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