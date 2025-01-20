from django.urls import path
from .views import product_list, product_detail, calculate_price

urlpatterns = [
    path('products/', product_list, name='product-list'),
    path('products/<int:pk>/', product_detail, name='product-detail'),
    path('products/<int:pk>/calculate-price/', calculate_price, name='calculate-price'),
]