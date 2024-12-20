from django.urls import path, include
from . import views

app_name = 'comments'

urlpatterns = [
    path('add/<int:product_id>/', views.CommentCreateView.as_view(), name='comment_add'),
    path('delete/<int:product_id>/<int:comment_id>/', views.CommentDeleteView.as_view(), name='comment_delete'),
]

