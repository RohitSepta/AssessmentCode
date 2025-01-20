from django.urls import path

from .views import order_list, order_detail, apply_discount_to_order

urlpatterns = [
    path('orders/', order_list, name='order-list'),
    path('orders/<int:pk>/', order_detail, name='order-detail'),
    path('orders/<int:pk>/apply-discount/', apply_discount_to_order, name='apply-discount-to-order'),
]