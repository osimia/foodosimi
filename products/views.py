from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Category
from cart.models import CartItem
from .forms import ProductForm, CategoryForm
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def my_products(request):
    """Отображение товаров текущего пользователя (продавца/мастера)"""
    if not hasattr(request.user, 'role') or request.user.role not in ['master', 'seller']:
        messages.error(request, 'У вас нет прав для просмотра этой страницы.')
        return redirect('products:product_list')
    
    # Получаем товары текущего пользователя
    products = Product.objects.filter(master=request.user).order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(products, 10)  # 10 товаров на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'title': 'Мои товары'
    }
    return render(request, 'products/my_products.html', context)

def product_list(request):
    category_id = request.GET.get('category')
    products = Product.objects.all().order_by('-created_at')
    # Показываем только категории, в которых есть товары
    categories = Category.objects.filter(
        id__in=Product.objects.exclude(category__isnull=True).values_list('category_id', flat=True).distinct()
    ).order_by('name')

    if category_id:
        products = products.filter(category_id=category_id)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

# Функция add_to_cart перемещена в cart/views.py для поддержки анонимных пользователей

@login_required
def product_add(request):
    if not hasattr(request.user, 'role') or request.user.role != 'master':
        return redirect('products:product_list')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, user=request.user)
        
        if form.is_valid():
            # Сохраняем продукт
            product = form.save(commit=False)
            product.master = request.user
            product.save()
            
            messages.success(request, 'Товар успешно создан!')
            return redirect('products:my_products')
        else:
            # Ошибки в форме
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Ошибка в поле {field}: {error}")
    else:
        form = ProductForm(user=request.user)
        
    return render(request, 'products/product_add.html', {
        'form': form
    })

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, master=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product, user=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно обновлён!')
            return redirect('products:my_products')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Ошибка в поле {field}: {error}")
    else:
        form = ProductForm(instance=product, user=request.user)
        
    return render(request, 'products/product_add.html', {
        'form': form,
        'edit_mode': True
    })
        
    return render(request, 'products/product_add.html', {
        'form': form,
        'formset': formset,
        'edit_mode': True,
        'product': product
    })

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, master=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Товар удалён!')
        return redirect('products:my_products')
    return redirect('products:my_products')

def product_table(request):
    """Отображение товаров в виде таблицы Excel"""
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category')
    
    products = Product.objects.select_related('category').all().order_by('-created_at')
    categories = Category.objects.all()

    # Фильтрация по поиску
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Фильтрация по категории
    if category_id:
        products = products.filter(category_id=category_id)

    # Пагинация
    paginator = Paginator(products, 20)  # 20 товаров на страницу
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': int(category_id) if category_id else None,
    }
    return render(request, 'products/product_table.html', context)

@login_required
def category_add(request):
    """Создание новой категории продавцом"""
    if not hasattr(request.user, 'role') or request.user.role != 'master':
        messages.error(request, 'Только продавцы могут создавать категории.')
        return redirect('products:product_list')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user
            category.is_global = False  # Пользовательские категории не глобальные
            category.save()
            messages.success(request, f'Категория "{category.name}" успешно создана!')
            return redirect('products:category_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Ошибка в поле {field}: {error}")
    else:
        form = CategoryForm()
        
    return render(request, 'products/category_add.html', {
        'form': form
    })

@login_required
def category_list(request):
    """Список категорий пользователя"""
    if not hasattr(request.user, 'role') or request.user.role != 'master':
        messages.error(request, 'Доступ запрещен.')
        return redirect('products:product_list')
    
    # Показываем только созданные пользователем категории
    user_categories = Category.objects.filter(created_by=request.user).order_by('name')
    
    context = {
        'user_categories': user_categories,
    }
    return render(request, 'products/category_list.html', context)

@login_required
def category_edit(request, pk):
    """Редактирование категории"""
    category = get_object_or_404(Category, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Категория "{category.name}" успешно обновлена!')
            return redirect('products:category_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Ошибка в поле {field}: {error}")
    else:
        form = CategoryForm(instance=category)
        
    return render(request, 'products/category_add.html', {
        'form': form,
        'edit_mode': True,
        'category': category
    })

@login_required
def category_delete(request, pk):
    """Удаление категории"""
    category = get_object_or_404(Category, pk=pk, created_by=request.user)
    
    # Проверяем, используется ли категория в товарах
    products_count = category.product_set.count()
    
    if request.method == 'POST':
        if products_count > 0:
            messages.error(request, f'Нельзя удалить категорию "{category.name}", так как она используется в {products_count} товарах. Сначала измените категорию для этих товаров.')
            return redirect('products:category_list')
        
        category_name = category.name
        category.delete()
        messages.success(request, f'Категория "{category_name}" удалена!')
        return redirect('products:category_list')
    
    return render(request, 'products/category_confirm_delete.html', {
        'category': category,
        'products_count': products_count
    })

@login_required
def category_add_ajax(request):
    """AJAX создание новой категории"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if not hasattr(request.user, 'role') or request.user.role != 'master':
            return JsonResponse({'success': False, 'message': 'Доступ запрещен'})
        
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user
            category.is_global = False
            category.save()
            
            return JsonResponse({
                'success': True, 
                'category_id': category.id,
                'category_name': category.name,
                'message': f'Категория "{category.name}" создана!'
            })
        else:
            errors = []
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f"{field}: {error}")
            return JsonResponse({'success': False, 'message': '; '.join(errors)})
    
    return JsonResponse({'success': False, 'message': 'Неверный запрос'})
