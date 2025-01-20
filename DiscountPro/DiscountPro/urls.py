from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product_info/',include('product_info.urls')),
    path('discount_info/',include('discount_info.urls')),
    path('order_info/',include('order_info.urls')),
]