#!/usr/bin/env python
import os
import sys
import django

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fruitsite.settings')
django.setup()

from products.models import Product

def check_products():
    """Проверяем товары и их новые поля"""
    print("=== ПРОВЕРКА ТОВАРОВ ===\n")
    
    products = Product.objects.all()
    
    if products:
        print(f"Найдено {len(products)} товаров:")
        print("-" * 80)
        
        for i, product in enumerate(products, 1):
            print(f"{i:2d}. {product.name}")
            print(f"    ID: {product.id}")
            print(f"    Цена: {product.price}")
            print(f"    Объем: '{product.volume}'")
            print(f"    Упаковка: '{product.package_type}'")
            print(f"    Кол-во в упаковке: {product.quantity_in_package}")
            print(f"    Цена за единицу: {product.price_per_unit}")
            print(f"    Цена за упаковку: {product.price_per_package}")
            print(f"    Мастер: {product.master}")
            print()
    else:
        print("Товары не найдены!")

if __name__ == '__main__':
    try:
        check_products()
    except Exception as e:
        print(f"Ошибка при проверке товаров: {e}")
        import traceback
        traceback.print_exc()
