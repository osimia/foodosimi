#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fruitsite.settings')
django.setup()

from products.models import Product
from decimal import Decimal

def update_products_with_sample_data():
    print("=== Обновление товаров с примерными данными ===")
    
    products = Product.objects.all()[:5]  # Возьмем первые 5 товаров
    
    sample_data = [
        {
            'volume': '500г',
            'package_type': 'Пластиковая упаковка',
            'quantity_in_package': 1,
            'price_per_unit': Decimal('150.00'),
            'price_per_package': Decimal('150.00'),
        },
        {
            'volume': '250г',
            'package_type': 'Картонная коробка',
            'quantity_in_package': 4,
            'price_per_unit': Decimal('75.00'),
            'price_per_package': Decimal('300.00'),
        },
        {
            'volume': '1кг',
            'package_type': 'Сетка',
            'quantity_in_package': 1,
            'price_per_unit': Decimal('200.00'),
            'price_per_package': Decimal('200.00'),
        },
        {
            'volume': '350г',
            'package_type': 'Стеклянная банка',
            'quantity_in_package': 6,
            'price_per_unit': Decimal('45.00'),
            'price_per_package': Decimal('270.00'),
        },
        {
            'volume': '750г',
            'package_type': 'Вакуумная упаковка',
            'quantity_in_package': 2,
            'price_per_unit': Decimal('120.00'),
            'price_per_package': Decimal('240.00'),
        },
    ]
    
    for i, product in enumerate(products):
        if i < len(sample_data):
            data = sample_data[i]
            product.volume = data['volume']
            product.package_type = data['package_type']
            product.quantity_in_package = data['quantity_in_package']
            product.price_per_unit = data['price_per_unit']
            product.price_per_package = data['price_per_package']
            product.save()
            
            print(f"Обновлен товар: {product.name}")
            print(f"  Объем: {product.volume}")
            print(f"  Упаковка: {product.package_type}")
            print(f"  Количество в упаковке: {product.quantity_in_package}")
            print(f"  Цена за единицу: {product.price_per_unit} сом")
            print(f"  Цена за упаковку: {product.price_per_package} сом")
            print("---")
    
    print(f"Обновлено {min(len(products), len(sample_data))} товаров")

if __name__ == "__main__":
    update_products_with_sample_data()
