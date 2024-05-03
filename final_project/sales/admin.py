from django.contrib import admin
from .models import CarSalesPost
from common.models import CustomUser, CarAPI,loan_rate_list
# Register your models here.
admin.site.register(CarSalesPost)
admin.site.register(CustomUser)
admin.site.register(CarAPI)
admin.site.register(loan_rate_list)