from django.urls import path

from .views import base_views, question_views, consume_views

app_name = 'sales'

urlpatterns = [ 
   # base_views.py
    path('',
         base_views.index, name='index'),
     path('my_page/', base_views.my_page, name='my_page'),
     
    path('propose_price/<int:post_id>/',
         consume_views.propose_price, name='propose_price'),

     
    path('detail/<int:post_id>/',
         base_views.detail, name='detail'),

    path('accept-proposal/<int:proposal_id>/',
         base_views.accept_proposal, name='accept_proposal'),
    
    path('cancel_proposal/<int:post_id>/',
         base_views.cancel_proposal, name='cancel_proposal'),
         
    path('detail/<int:post_id>/show_loan_table/', 
         base_views.show_loan_table, name='show_loan_table'),

    # question_views.py
    path('create/<str:car_VNUM>/',
         question_views.question_create, name='question_create'),
    path('modify/<int:post_id>/',
         question_views.sales_modify, name='sales_modify'),
    path('delete/<int:post_id>/',
         question_views.sales_delete, name='sales_delete'),

    path('buy/<int:post_id>/', question_views.buy_car, name='buy_car'),
]   