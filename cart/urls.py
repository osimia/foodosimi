# fruitsite/cart/urls.py

from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add-ajax/', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:pk>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('count/', views.get_cart_count, name='get_cart_count'),
]
