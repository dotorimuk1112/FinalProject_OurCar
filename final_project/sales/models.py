from django.db import models
from common.models import CustomUser
from config.settings import MEDIA_ROOT
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

class CarSalesPost(models.Model):
    post_id = models.AutoField(primary_key=True)  # 자동으로 1씩 증가하는 필드로 지정
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_question')
    # subject = models.CharField(max_length=300) ## 제목은 MNAME 으로 일단 대체해볼게요
    ############차량 상세정보 ##############
    MNAME = models.TextField(null=False)
    MYERAR = models.IntegerField(null=False)
    MILEAGE = models.IntegerField(null=False)
    COLOR = models.TextField(null=False)
    TRANS = models.TextField(null=False)
    F_TYPE = models.TextField(null=False)
    DISP = models.IntegerField(null=False)
    VTYPE = models.TextField(null=False)
    VNUM = models.CharField(max_length=100)  # 적절한 길이를 선택하세요.
    CU_HIS = models.IntegerField(null=False)
    MVD_HIS = models.FloatField(null=False)
    AVD_HIS = models.FloatField(null=False)
    FD_HIS = models.IntegerField(null=False)
    VT_HIS = models.FloatField(null=False)
    US_HIS = models.IntegerField(null=False)
    #######################################
    PRICE = models.IntegerField(null=False) ##만원단위
    modify_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField()

    buyer = models.ManyToManyField(CustomUser, related_name='buyer_car_sales_posts')  # 추천인 추가
    brand = models.TextField(null=True)
    thumbnail_image = models.ImageField(upload_to='vehicle_images', blank=True, null=True)
    Image1 = models.ImageField(upload_to='vehicle_images', blank=True, null=True)
    Image2 = models.ImageField(upload_to='vehicle_images', blank=True, null=True)
    Image3 = models.ImageField(upload_to='vehicle_images', blank=True, null=True)
    Image4 = models.ImageField(upload_to='vehicle_images', blank=True, null=True)
    
    detected_thumbnail = models.ImageField(upload_to='detected_results', blank=True, null=True)
    detected_image1 = models.ImageField(upload_to='detection_results', blank=True, null=True)
    detected_image2 = models.ImageField(upload_to='detection_results', blank=True, null=True)
    detected_image3 = models.ImageField(upload_to='detection_results', blank=True, null=True)
    detected_image4 = models.ImageField(upload_to='detection_results', blank=True, null=True)
    buyers_count = models.IntegerField(default=0)
    def __str__(self):
        return self.MNAME
    
@receiver(post_save, sender='sales.BuyerMessages')
@receiver(post_delete, sender='sales.BuyerMessages')
def update_buyers_count(sender, instance, **kwargs):
    buyers_count = BuyerMessages.objects.filter(post_id=instance.post_id).count()
    CarSalesPost.objects.filter(post_id=instance.post_id).update(buyers_count=buyers_count)


# class Answer(models.Model):
#     author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_answer')
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     content = models.TextField()
#     modify_date = models.DateTimeField(null=True, blank=True)
#     create_date = models.DateTimeField()
#     voter = models.ManyToManyField(CustomUser, related_name='voter_answer')
    
# class UploadedImage(models.Model):
#     uploadedimage = models.ImageField(upload_to=f'{MEDIA_ROOT}')
#     processedimage = models.ImageField(upload_to=f'{MEDIA_ROOT}')
#     has_car = models.BooleanField(default=False)
#     is_processed = models.BooleanField(default=False)


class UploadedImage2(models.Model):
    uploadedimage = models.ImageField(upload_to=f'{MEDIA_ROOT}')
    processedimage = models.ImageField(upload_to=f'{MEDIA_ROOT}')  # processedimage 필드 추가
    has_car = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'pybo_uploadedimage2'

class BuyerMessages(models.Model):
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='buyer_messages', null=False)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='seller_messages', null=False)
    post = models.ForeignKey(CarSalesPost, on_delete=models.CASCADE, related_name='post_messages', null=False)
    buyer_price = models.IntegerField(null=False)  # 만원단위
    accepted = models.BooleanField(null=True)  # 수락 여부를 저장할 필드

    class Meta: 
        managed = True
        db_table = 'BuyerMessages'