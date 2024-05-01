from django.db import models
from common.models import CustomUser
from config.settings import MEDIA_URL
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

class CarSalesPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_question')
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
    Image5 = models.ImageField(upload_to='vehicle_images', blank=True, null=True)
    Image6 = models.ImageField(upload_to='vehicle_images', blank=True, null=True)
    Image7 = models.ImageField(upload_to='vehicle_images', blank=True, null=True)
    Image8 = models.ImageField(upload_to='vehicle_images', blank=True, null=True)
    
    detected_thumbnail = models.ImageField(upload_to='detected_results', blank=True, null=True)
    detected_image1 = models.ImageField(upload_to='detection_results', blank=True, null=True)
    detected_image2 = models.ImageField(upload_to='detection_results', blank=True, null=True)
    detected_image3 = models.ImageField(upload_to='detection_results', blank=True, null=True)
    detected_image4 = models.ImageField(upload_to='detection_results', blank=True, null=True)
    detected_image5 = models.ImageField(upload_to='detection_results', blank=True, null=True)
    detected_image6 = models.ImageField(upload_to='detection_results', blank=True, null=True)
    detected_image7 = models.ImageField(upload_to='detection_results', blank=True, null=True)
    detected_image8 = models.ImageField(upload_to='detection_results', blank=True, null=True)
    buyers_count = models.IntegerField(default=0)
    make_deal = models.BooleanField(default=False)  # 새로 추가된 필드

    def __str__(self):
        return self.MNAME
    
@receiver(post_save, sender='sales.BuyerMessages')
@receiver(post_delete, sender='sales.BuyerMessages')
def update_buyers_count(sender, instance, **kwargs):
    buyers_count = BuyerMessages.objects.filter(post_id=instance.post_id).count()
    CarSalesPost.objects.filter(post_id=instance.post_id).update(buyers_count=buyers_count)

class BuyerMessages(models.Model):
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='buyer_messages', null=False)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='seller_messages', null=False)
    post = models.ForeignKey(CarSalesPost, on_delete=models.CASCADE, related_name='post_messages', null=False)
    buyer_price = models.IntegerField(null=False)  # 만원단위
    accepted = models.BooleanField(null=True)  # 수락 여부를 저장할 필드

    class Meta: 
        managed = True
        db_table = 'BuyerMessages'
        
@receiver([post_save, post_delete], sender=BuyerMessages)
def update_make_deal(sender, instance, **kwargs):
    # 해당 게시물에 대한 BuyerMessages의 accepted가 True인 수를 가져옵니다.
    accepted_count = BuyerMessages.objects.filter(post=instance.post, accepted=True).count()
    # 만약 accepted가 1 이상이면 make_deal 값을 True로 설정합니다.
    if accepted_count > 0:
        CarSalesPost.objects.filter(post_id=instance.post.post_id).update(make_deal=True)
    else:
        # accepted가 없으면 make_deal 값을 False로 설정합니다.
        CarSalesPost.objects.filter(post_id=instance.post.post_id).update(make_deal=False)