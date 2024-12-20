from django.urls import path

from account.urls import urlpatterns
from . import views

app_name = 'coupons'

urlpatterns=[
    path('apply/', views.CouponApplyView.as_view(), name='apply'),
]