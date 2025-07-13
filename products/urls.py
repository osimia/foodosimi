from django.urls import path
from . import views
from . import views_debug

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('table/', views.product_table, name='product_table'),
    path('my-products/', views.my_products, name='my_products'),
    path('add/', views.product_add, name='product_add'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # URL для категорий
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/add-ajax/', views.category_add_ajax, name='category_add_ajax'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Диагностические URL (только для администраторов)
    path('debug/check-s3-images/', views_debug.check_s3_images, name='check_s3_images'),
    path('debug/test-s3-images/', views_debug.test_s3_images, name='test_s3_images'),
]
