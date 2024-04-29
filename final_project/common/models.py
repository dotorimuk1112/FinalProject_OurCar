
from django.db import models
from django.contrib.auth.models import AbstractUser



class TestSangmin(models.Model):
    id = models.AutoField(primary_key=True)
    seq = models.CharField(max_length=255, blank=True, null=True)
    interior_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    interior_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    insuhos_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    offedu_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    trvlec_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    fsbz_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    svcarc_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    dist_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    plsanit_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    clothgds_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    auto_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    car_price = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    real_name = models.CharField(max_length=100)  # 예시로 최대 길이 100으로 설정했습니다.
    address = models.CharField(max_length=255, blank=True, null=True)  # 새로 추가한 address 필드
    class GenderChoices(models.TextChoices):
        MALE = 'M', '남성'
        FEMALE = 'F', '여성'
    gender = models.CharField(choices=GenderChoices.choices, max_length=1, blank=True,null=True)
    test_sangmin = models.OneToOneField(TestSangmin, on_delete=models.CASCADE, related_name='custom_user', blank=True, null=True)

    
class Car(models.Model):
    SEQ = models.IntegerField()
    MNAME = models.TextField()
    PRICE = models.IntegerField()
    MYERAR = models.IntegerField()
    MILEAGE = models.IntegerField()
    COLOR = models.TextField()
    TRANS = models.TextField()
    F_TYPE = models.TextField()
    DISP = models.IntegerField()
    VTYPE = models.TextField()
    VNUM = models.CharField(max_length=100, primary_key=True)  # 적절한 길이를 선택하세요.
    CU_HIS = models.IntegerField()
    MVD_HIS = models.FloatField()
    AVD_HIS = models.FloatField()
    FD_HIS = models.IntegerField()
    VT_HIS = models.FloatField()
    US_HIS = models.IntegerField()
    L_NAME = models.TextField(null=True)  # nullable로 설정


class predict_budget(models.Model):
    id = models.AutoField(primary_key=True)
    seq = models.CharField(max_length=255, blank=True, null=True)
    interior_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    insuhos_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    offedu_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    trvlec_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    fsbz_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    svcarc_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    dist_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    plsanit_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    clothgds_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    auto_am = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)

class scoring(models.Model):
    id = models.AutoField(primary_key=True)
    verification_status = models.BooleanField()
    home_ownership = models.CharField(max_length=255)
    loan_amnt = models.IntegerField()
    int_rate = models.DecimalField(max_digits=7, decimal_places=2)
    term = models.CharField(max_length=255)
    purpose = models.CharField(max_length=255)
    annual_inc = models.DecimalField(max_digits=10, decimal_places=2)
    dti = models.DecimalField(max_digits=7, decimal_places=2)
    avg_cur_bal = models.IntegerField()
    acc_open_past_24mths = models.IntegerField()
    total_bc_limit = models.IntegerField()
    bc_util = models.DecimalField(max_digits=5, decimal_places=1)
    last_avg_fico = models.DecimalField(max_digits=4, decimal_places=1)
    avg_fico = models.DecimalField(max_digits=4, decimal_places=1)
    
class loan_rate_list(models.Model):
    company_name = models.CharField(max_length=255)
    min_rate = models.FloatField()
    max_rate = models.FloatField()
    pq_avg_act_rate = models.CharField(max_length=255)  # 수정된 부분
    erc_rate = models.CharField(max_length=255)
    late_payment_rate = models.CharField(max_length=255)
    reference_date = models.DateField()
    credit_range = models.IntegerField()
    loan_period = models.IntegerField()
    link = models.TextField(null=True)