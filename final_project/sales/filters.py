import django_filters
from .models import CarSalesPost

class CarSalesPostFilter(django_filters.FilterSet):
    class Meta:
        model = CarSalesPost
        fields = {
            'PRICE': ['gte', 'lte'],  # 가격의 범위 필터
            'MNAME': ['icontains'],    # 모델 이름에 대한 일치하는 문자열 필터 (대소문자 무시)
        }