from django.urls import path

from .views import base_views, question_views
from sales.views import car_determination_views


app_name = 'sales'

urlpatterns = [ 
   # base_views.py
    path('',
         base_views.index, name='index'),
     path('my_page/', base_views.my_page, name='my_page'),
    

     
    path('detail/<int:post_id>/',
         base_views.detail, name='detail'),

    # question_views.py
    path('create/<str:car_VNUM>/',
         question_views.question_create, name='question_create'),
    path('modify/<int:question_id>/',
         question_views.question_modify, name='question_modify'),
    path('delete/<int:question_id>/',
         question_views.question_delete, name='question_delete'),

    path('vote/<int:question_id>/', question_views.question_vote, name='question_vote'),
    
    

        # car_determination_views.py
    path('car_determination/', 
         car_determination_views.car_determination, name='car_determination'),  # '/' 에 해당되는 path
    

]   