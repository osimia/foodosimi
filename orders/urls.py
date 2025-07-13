# fruitsite/orders/urls.py

from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('my/', views.my_orders, name='my_orders'),
    path('find/', views.find_orders, name='find_orders'),
    path('seller/', views.seller_orders, name='seller_orders'),
    path('accept/<int:order_id>/', views.accept_order, name='accept_order'),
    path('reject/<int:order_id>/', views.reject_order, name='reject_order'),
    path('update/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('confirm-delivery/<int:order_id>/', views.confirm_delivery, name='confirm_delivery'),
    path('download-invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
]
