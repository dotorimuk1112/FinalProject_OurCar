from ..models import BuyerMessages, CarSalesPost
from ..forms import BuyerMessagesForm
from django.shortcuts import render, redirect, get_object_or_404

def propose_price(request, post_id):
    current_post = get_object_or_404(CarSalesPost, post_id=post_id)
    
    if request.method == 'POST':
        form = BuyerMessagesForm(request.POST)
        if form.is_valid():
            # 입력된 데이터
            buyer_price = form.cleaned_data['buyer_price']
            # 기존의 레코드가 있는지 확인
            existing_record = BuyerMessages.objects.filter(buyer_id=request.user.id, post_id=current_post.post_id).first()
            if existing_record:
                # 기존의 레코드가 있으면 수정
                existing_record.buyer_price = buyer_price
                existing_record.accepted = None
                existing_record.save()
            else:
                # 기존의 레코드가 없으면 새로 생성
                buyer_message = form.save(commit=False)
                buyer_message.buyer_id = request.user.id
                buyer_message.post_id = current_post.post_id
                buyer_message.seller_id = current_post.seller.id
                buyer_message.accepted = None
                buyer_message.save()
            # 데이터가 성공적으로 저장된 후 리디렉션할 URL
            return redirect('sales:my_page')  # 사용자가 자신의 페이지로 리디렉션하도록 수정해야 할 수도 있습니다.
    else:
        form = BuyerMessagesForm()
    
    return render(request, 'sales/propose_price.html', {'form': form, 'current_post': current_post})
