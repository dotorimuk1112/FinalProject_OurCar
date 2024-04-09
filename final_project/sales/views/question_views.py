from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..forms import SalesForm
from ..models import CarSalesPost
from common.models import Car

# from ..forms import QuestionForm
# from ..models import Question

# 질문 생성
@login_required(login_url='common:login')
def question_create(request, car_VNUM):
    car = get_object_or_404(Car, VNUM=car_VNUM)

    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            CarSalesPost = form.save(commit=False)
            CarSalesPost.seller = request.user
            CarSalesPost.create_date = timezone.now()
            CarSalesPost.save()
            return redirect('sales:index')
    else:
        form = SalesForm()
    context = {'form': form, 'car': car}  # Pass the car object to the template
    return render(request, 'sales/question_form.html', context)



# 질문 수정
@login_required(login_url='common:login')
def question_modify(request, post_id):
    CarSalesPost = get_object_or_404(CarSalesPost, pk=post_id)
    if request.user != CarSalesPost.seller:
        messages.error(request, '수정권한이 없습니다')
        return redirect('sales:detail', question_id=CarSalesPost.post_id)
    if request.method == "POST":
        form = SalesForm(request.POST, instance=CarSalesPost)
        if form.is_valid():
            CarSalesPost = form.save(commit=False)
            CarSalesPost.modify_date = timezone.now()  # 수정일시 저장
            CarSalesPost.save()
            return redirect('sales:detail', question_id=CarSalesPost.post_id)
    else:
        form = SalesForm(instance=CarSalesPost)
    context = {'form': form}
    return render(request, 'sales/question_form.html', context)

# 질문 삭제
@login_required(login_url='common:login')
def question_delete(request, post_id):
    CarSalesPost = get_object_or_404(CarSalesPost, pk=post_id)
    if request.user != CarSalesPost.seller:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('sales:detail', post_id=CarSalesPost.post_id)
    CarSalesPost.delete()
    return redirect('sales:index')

# 질문 추천
@login_required(login_url='common:login')
def question_vote(request, post_id):
    CarSalesPost = get_object_or_404(CarSalesPost, pk=post_id)
    if request.user == CarSalesPost.seller:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        CarSalesPost.voter.add(request.user)
    return redirect('sales:detail', post_id=CarSalesPost.post_id)