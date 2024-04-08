
from django.db import models
from django.contrib.auth.models import AbstractUser



class TestSangmin(models.Model):
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
    car_price = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'test_sangmin'

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    test_sangmin = models.OneToOneField(TestSangmin, on_delete=models.CASCADE, related_name='custom_user', blank=True, null=True)
