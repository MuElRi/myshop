from django.urls import path

from . import views


app_name = 'orders'

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('admin/order/<int:pk>/', views.AdminOrderDetailView.as_view(),
                                        name='admin_order_detail'),
    path('admin/order/<int:pk>/pdf/', views.AdminOrderPDFView.as_view(),
                                        name='admin_order_pdf'),
    path('created/', views.OrderStatusView.as_view(), name='order_status'),
    # path('pay_again', views.order_pay_again, name='pay_again'),
    path('order_history/', views.OrderListView.as_view(), name='order_list'),
]