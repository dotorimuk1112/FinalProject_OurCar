from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..forms import SalesForm
from ..models import CarSalesPost
from common.models import Car
from PIL import Image
from ..static.car_determination import car_determination
from django.http import HttpResponse

# 질문 생성
@login_required(login_url='common:login')
def question_create(request, car_VNUM):
    car = get_object_or_404(Car, VNUM=car_VNUM)
    if request.method == 'POST':
        form = SalesForm(request.POST, request.FILES)
        if form.is_valid():
            car_sales_post = form.save(commit=False)
            car_sales_post.seller = request.user
            car_sales_post.create_date = timezone.now()
            
            # ■업로드 이미지 처리 
            # 썸네일 처리
            not_car_list = []

            thumb = request.FILES.get("thumbnail_image")
            thumbnail_img_result = car_determination(thumb)
            if thumb and (thumbnail_img_result=='2'):
                car_sales_post.thumbnail_image = thumb
                print('썸네일 자동차 확인. 업로드 성공.')
            else:
                not_car_list.append('썸네일')
                
            # 이미지1 처리
            image1 = request.FILES.get("image1")
            img1_result = car_determination(image1)
            if image1 and (img1_result == '2'):
                car_sales_post.Image1 = image1
                print('1번 이미지 자동차 확인. 업로드 성공.')
            else:
                not_car_list.append('이미지1')

            # 이미지2 처리
            image2 = request.FILES.get("image2")
            img2_result = car_determination(image2)
            if image2 and (img2_result == '2'):
                car_sales_post.Image2 = image2
            else:
                not_car_list.append('이미지2')

            # 이미지3 처리
            image3 = request.FILES.get("image3")
            img3_result = car_determination(image3)
            if image3 and (img3_result == '2'):
                car_sales_post.Image3 = image3
            else:
                not_car_list.append('이미지3')

            # 이미지4 처리
            image4 = request.FILES.get("image4")
            img4_result = car_determination(image4)
            if image4 and (img4_result == '2'):
                car_sales_post.Image4 = image4
            else:
                not_car_list.append('이미지4')

            if not_car_list:
                error_messages = [f'{m}에 자동차가 포함되어 있지 않습니다.' for m in not_car_list]
                for error_message in error_messages:
                    messages.error(request, error_message)
                context = {'form': form, 'car': car, 'error_messages': error_messages}
                return render(request, 'sales/question_form.html', context)

            car_sales_post.save()
            messages.success(request, '판매 게시글이 성공적으로 등록됐습니다.')
            return redirect('sales:index')
    else:
        form = SalesForm()
    context = {'form': form, 'car': car}
    return render(request, 'sales/question_form.html', context)



# 질문 수정
@login_required(login_url='common:login')
def sales_modify(request, post_id):
    car_sales_post = get_object_or_404(CarSalesPost, pk=post_id)
    if request.user != car_sales_post.seller:
        messages.error(request, '수정권한이 없습니다')
        return redirect('sales:detail', post_id=car_sales_post.post_id)
    if request.method == "POST":
        form = SalesForm(request.POST, instance=car_sales_post)

        if form.is_valid():
            car_sales_post = form.save(commit=False)
            car_sales_post.modify_date = timezone.now()  # 수정일시 저장
            car_sales_post.save()
            return redirect('sales:detail', post_id=car_sales_post.post_id)
    else:
        form = SalesForm(instance=car_sales_post)
      # car 변수에 차량번호 정보를 저장
    car_VNUM = car_sales_post.VNUM
    car = get_object_or_404(Car, VNUM=car_VNUM)
    context = {'form': form, 'car_sales_post': car_sales_post, 'car': car}
    return render(request, 'sales/question_form.html', context)


# 판매글 삭제
@login_required(login_url='common:login')
def sales_delete(request, post_id):
    car_sales_post = get_object_or_404(CarSalesPost, pk=post_id)
    if request.user != car_sales_post.seller:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('sales:detail', post_id=car_sales_post.post_id)
    car_sales_post.delete()
    return redirect('sales:index')

# 질문 추천
# @login_required(login_url='common:login')
# def question_vote(request, post_id):
#     CarSalesPost = get_object_or_404(CarSalesPost, pk=post_id)
#     if request.user == CarSalesPost.seller:
#         messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
#     else:
#         CarSalesPost.voter.add(request.user)
#     return redirect('sales:detail', post_id=CarSalesPost.post_id)

# 차량 구매 요청
@login_required(login_url='common:login')
def buy_car(request, post_id):
    car_sales_post = get_object_or_404(CarSalesPost, pk=post_id)
    if request.user == car_sales_post.seller:
        messages.error(request, '본인이 판매하는 차량은 구매할 수 없습니다.')
    elif request.user in car_sales_post.buyer.all():  # 이미 구매 요청을 한 경우
        car_sales_post.buyer.remove(request.user)  # 구매 요청 취소
    else:
        car_sales_post.buyer.add(request.user)  # 구매 요청 추가
    return redirect('sales:detail', post_id=car_sales_post.post_id)