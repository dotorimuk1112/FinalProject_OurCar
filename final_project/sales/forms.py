from django import forms
from sales.models import CarSalesPost, BuyerMessages
from common.models import CustomUser


class SalesForm(forms.ModelForm):
    class Meta:
        model = CarSalesPost
        fields = ['PRICE', 'MNAME', 'MYERAR', 'MILEAGE', 'COLOR', 'TRANS', 'F_TYPE', 'DISP', 'VTYPE', 'VNUM', 'CU_HIS', 'MVD_HIS', 'AVD_HIS', 'FD_HIS', 'VT_HIS', 'US_HIS', 'thumbnail_image']
        labels = {
            'PRICE': '가격',
            'MNAME': '모델명',
            'MYERAR': '연식',
            'MILEAGE': '주행거리',
            'COLOR': '색상',
            'TRANS': '변속기',
            'F_TYPE': '연료',
            'DISP': '배기량',
            'VTYPE': '차종',
            'VNUM': '차량번호',
            'CU_HIS': '용도변경 이력',
            'MVD_HIS': '자차피해 이력',
            'AVD_HIS': '타차피해 이력',
            'FD_HIS': '침수 이력',
            'VT_HIS': '도난 이력',
            'US_HIS': '소유자 변경 횟수',
            'thumbnail_image': '이미지'
        }

    
# class VehicleImageForm(forms.ModelForm):
#     class Meta:
#         model = CarSalesPost
#         fields = ['thumbnail_image', 'Image1', 'Image2', 'Image3', 'Image4']

        
class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image']
        

class BuyerMessagesForm(forms.ModelForm):
    class Meta:
        model = BuyerMessages
        fields = ['buyer_price']