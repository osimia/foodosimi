# duzanda/cart/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import CartItem
from products.models import Product

def get_cart_owner_info(request):
    """Получает информацию о владельце корзины (пользователь или сессия)"""
    if request.user.is_authenticated:
        return {'buyer': request.user}, {'buyer': request.user}
    else:
        # Убедимся, что у нас есть ключ сессии
        if not request.session.session_key:
            request.session.create()
        return {'session_key': request.session.session_key}, {'session_key': request.session.session_key}

def view_cart(request):
    owner_filter, _ = get_cart_owner_info(request)
    
    cart_items = CartItem.objects.filter(**owner_filter)
    total = sum(item.get_total_price() for item in cart_items)
    
    return render(request, 'cart/cart_view.html', {
        'cart_items': cart_items,
        'total': total,
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    unit_type = request.POST.get('unit_type', 'unit')  # 'unit' или 'package'
    
    owner_filter, owner_data = get_cart_owner_info(request)
    
    # Проверяем, есть ли уже такой товар с такой же единицей измерения в корзине
    existing_item = CartItem.objects.filter(
        product=product, 
        unit_type=unit_type,
        **owner_filter
    ).first()
    
    if existing_item:
        existing_item.quantity += quantity
        existing_item.save()
        unit_display = dict(CartItem.UNIT_CHOICES)[unit_type]
        messages.success(request, f"Количество товара {product.name} ({unit_display}) обновлено в корзине.")
    else:
        CartItem.objects.create(
            product=product,
            quantity=quantity,
            unit_type=unit_type,
            **owner_data
        )
        unit_display = dict(CartItem.UNIT_CHOICES)[unit_type]
        messages.success(request, f"Товар {product.name} ({unit_display}) добавлен в корзину.")
    
    return redirect('products:product_detail', pk=product_id)

def remove_from_cart(request, pk):
    owner_filter, _ = get_cart_owner_info(request)
    item = get_object_or_404(CartItem, pk=pk, **owner_filter)
    item.delete()
    messages.success(request, "Товар удален из корзины.")
    return redirect('cart:view_cart')

def update_quantity(request, pk, action):
    owner_filter, _ = get_cart_owner_info(request)
    item = get_object_or_404(CartItem, pk=pk, **owner_filter)
    
    if action == 'increase':
        item.quantity += 1
        messages.success(request, "Количество товара увеличено.")
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1
        messages.success(request, "Количество товара уменьшено.")
    
    item.save()
    return redirect('cart:view_cart')

@require_POST
def add_to_cart_ajax(request):
    """AJAX-обработчик для добавления товара в корзину из таблицы"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        unit_type = data.get('unit_type', 'unit')
        
        product = get_object_or_404(Product, id=product_id)
        
        # Проверяем наличие товара
        if quantity > product.stock:
            return JsonResponse({
                'success': False,
                'message': f'В наличии только {product.stock} шт.'
            })
        
        owner_filter, owner_data = get_cart_owner_info(request)
        
        # Проверяем, есть ли уже такой товар с такой же единицей измерения в корзине
        existing_item = CartItem.objects.filter(
            product=product, 
            unit_type=unit_type,
            **owner_filter
        ).first()
        
        if existing_item:
            new_quantity = existing_item.quantity + quantity
            if new_quantity > product.stock:
                return JsonResponse({
                    'success': False,
                    'message': f'Превышено количество в наличии. В корзине уже {existing_item.quantity} шт.'
                })
            existing_item.quantity = new_quantity
            existing_item.save()
        else:
            CartItem.objects.create(
                product=product,
                quantity=quantity,
                unit_type=unit_type,
                **owner_data
            )
        
        unit_display = dict(CartItem.UNIT_CHOICES)[unit_type]
        return JsonResponse({
            'success': True,
            'message': f'Товар "{product.name}" ({unit_display}) добавлен в корзину'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Произошла ошибка при добавлении товара'
        })

def get_cart_count(request):
    """API endpoint для получения количества товаров в корзине"""
    owner_filter, _ = get_cart_owner_info(request)
    cart_items = CartItem.objects.filter(**owner_filter)
    count = sum(item.quantity for item in cart_items)
    
    return JsonResponse({'count': count})
