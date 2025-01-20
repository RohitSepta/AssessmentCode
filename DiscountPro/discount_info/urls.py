from django.urls import path
from .views import discount_list, discount_detail, calculate_discount

urlpatterns = [
    path('discounts/', discount_list, name='discount-list'),
    path('discounts/<int:pk>/', discount_detail, name='discount-detail'),
    path('discounts/<int:pk>/calculate/', calculate_discount, name='calculate-discount'),
]