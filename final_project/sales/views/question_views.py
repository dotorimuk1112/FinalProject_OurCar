from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..forms import SalesForm
from ..models import CarSalesPost
from common.models import CarAPI
from PIL import Image
from ..static.car_models import car_determination_and_damage_detection

# 질문 생성
@login_required(login_url='common:login')
def question_create(request, car_VNUM):
    car = get_object_or_404(CarAPI, VNUM=car_VNUM)
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
            print(thumb)
            thumbnail_img_result, damage_thumbnail = car_determination_and_damage_detection(thumb)
            print(thumbnail_img_result, damage_thumbnail)
            if thumb:
                if thumbnail_img_result and ('2' in thumbnail_img_result):
                    car_sales_post.thumbnail_image = thumb
                    print('썸네일 자동차 확인. 업로드 성공.')
                    if damage_thumbnail:
                        car_sales_post.detected_thumbnail = damage_thumbnail
                        print('썸네일에서 차량 파손 감지')
                else:
                    not_car_list.append('대표 사진')
            else:
                not_car_list.append('대표 사진')
                
            # 이미지1 처리
            image1 = request.FILES.get("image1")
            print(image1)
            img1_result, damage_result1 = car_determination_and_damage_detection(image1)
            print(img1_result, damage_result1)
            if image1:
                if img1_result and ( '2' in img1_result):
                    car_sales_post.Image1 = image1
                    print('1번 이미지 자동차 확인. 업로드 성공.')
                    if damage_result1:
                        car_sales_post.detected_image1 = damage_result1
                        print('1번 이미지에서 차량 파손 감지')
                else:
                    not_car_list.append('차량 전방 사진')
            else:
                not_car_list.append('차량 전방 사진')

            # 이미지2 처리
            image2 = request.FILES.get("image2")
            img2_result, damage_result2 = car_determination_and_damage_detection(image2)
            print(img2_result, damage_result2)
            if image2:
                if img2_result and ('2' in img2_result):
                    car_sales_post.Image2 = image2
                    print('2번 이미지 자동차 확인. 업로드 성공.')
                    if damage_result2:
                        car_sales_post.detected_image2 = damage_result2
                        print('2번 이미지에서 차량 파손 감지')
                else:
                    not_car_list.append('차량 좌측 사진')
            else:
                not_car_list.append('차량 좌측 사진')

            # 이미지3 처리
            image3 = request.FILES.get("image3")
            img3_result, damage_result3 = car_determination_and_damage_detection(image3)
            print(img3_result, damage_result3)
            if image3:
                if img3_result and ('2' in img3_result):
                    car_sales_post.Image3 = image3
                    print('3번 이미지 자동차 확인. 업로드 성공.')
                    if damage_result3:
                        car_sales_post.detected_image3 = damage_result3
                        print('3번 이미지에서 차량 파손 감지')
                else:
                    not_car_list.append('차량 우측 사진')
            else:
                not_car_list.append('차량 우측 사진')

            # 이미지4 처리
            image4 = request.FILES.get("image4")
            img4_result, damage_result4 = car_determination_and_damage_detection(image4)
            print(img4_result, damage_result4)
            if image4:
                if img4_result and ('2' in img4_result):
                    car_sales_post.Image4 = image4
                    print('4번 이미지 자동차 확인. 업로드 성공.')
                    if damage_result4:
                        car_sales_post.detected_image4 = damage_result4
                        print('4번 이미지에서 차량 파손 감지')
                else:
                    not_car_list.append('차량 후방 사진')
            else:
                not_car_list.append('차량 후방 사진')

            image5 = request.FILES.get("image5")
            img5_result, damage_result5 = car_determination_and_damage_detection(image5)
            print(img5_result, damage_result5)
            if image5:
                if img5_result and ('2' in img5_result):
                    car_sales_post.Image5 = image5
                    print('5번 이미지 자동차 확인. 업로드 성공.')
                    if damage_result5:
                        car_sales_post.detected_image5 = damage_result5
                        print('5번 이미지에서 차량 파손 감지')
                else:
                    not_car_list.append('차량 내부 사진')
            else:
                not_car_list.append('차량 내부 사진')

            image6 = request.FILES.get("image6")
            img6_result, damage_result6 = car_determination_and_damage_detection(image6)
            print(img6_result, damage_result6)
            if image6:
                if img6_result and ('2' in img6_result):
                    car_sales_post.Image6 = image6
                    print('6번 이미지 자동차 확인. 업로드 성공.')
                    if damage_result6:
                        car_sales_post.detected_image6 = damage_result6
                        print('6번 이미지에서 차량 파손 감지')
                else:
                    not_car_list.append('차량 대각 방향1')
            else:
                not_car_list.append('차량 대각 방향1')

            image7 = request.FILES.get("image7")
            img7_result, damage_result7 = car_determination_and_damage_detection(image7)
            print(img7_result, damage_result7)
            if image7:
                if img7_result and ('2' in img7_result):
                    car_sales_post.Image7 = image7
                    print('7번 이미지 자동차 확인. 업로드 성공.')
                    if damage_result7:
                        car_sales_post.detected_image7 = damage_result7
                        print('7번 이미지에서 차량 파손 감지')
                else:
                    not_car_list.append('차량 대각 방향2')
            else:
                not_car_list.append('차량 대각 방향2')

            image8 = request.FILES.get("image8")
            img8_result, damage_result8 = car_determination_and_damage_detection(image8)
            print(img8_result, damage_result8)
            if image8:
                if img8_result:
                    car_sales_post.Image8 = image8
                    print('8번 이미지 자동차 확인. 업로드 성공.')
                    if damage_result8:
                        car_sales_post.detected_image8 = damage_result8
                        print('8번 이미지에서 차량 파손 감지')
                else:
                    not_car_list.append('엔진룸')
            else:
                not_car_list.append('엔진룸')

            if not_car_list:
                error_messages = [f'{m}에 자동차가 포함되어 있지 않습니다.' for m in not_car_list]
                for error_message in error_messages:
                    messages.error(request, error_message)
                context = {'form': form, 'car': car, 'error_messages': error_messages}
                return render(request, 'sales/question_form.html', context)
            else:
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
    car = get_object_or_404(CarAPI, VNUM=car_VNUM)
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