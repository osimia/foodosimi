#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fruitsite.settings')
django.setup()

from products.models import Product
from django.db import connection

def check_product_fields():
    print("=== Проверка полей модели Product ===")
    
    # Получаем все поля модели
    fields = Product._meta.get_fields()
    for field in fields:
        print(f"Поле: {field.name} - Тип: {type(field).__name__}")
    
    print("\n=== Проверка структуры таблицы в БД ===")
    
    # Получаем описание таблицы из базы данных
    with connection.cursor() as cursor:
        cursor.execute("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'products_product' ORDER BY ordinal_position;")
        columns = cursor.fetchall()
        
        for column in columns:
            print(f"Столбец: {column[0]} - Тип: {column[1]} - Nullable: {column[2]}")
    
    print("\n=== Проверка данных ===")
    
    # Проверяем количество товаров
    count = Product.objects.count()
    print(f"Всего товаров в БД: {count}")
    
    # Показываем первые несколько товаров с новыми полями
    if count > 0:
        print("\nПервые 3 товара с новыми полями:")
        for product in Product.objects.all()[:3]:
            print(f"ID: {product.id}")
            print(f"  Название: {product.name}")
            print(f"  Объем: {product.volume}")
            print(f"  Вид упаковки: {product.package_type}")
            print(f"  Количество в упаковке: {product.quantity_in_package}")
            print(f"  Цена за единицу: {product.price_per_unit}")
            print(f"  Цена за упаковку: {product.price_per_package}")
            print("---")

if __name__ == "__main__":
    check_product_fields()
