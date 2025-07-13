import os
import django
import sys

# Настраиваем Django
sys.path.append('c:/Users/Hp/Desktop/Новая папка/fruitsite')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fruitsite.settings')
django.setup()

from products.models import Product, Category
from accounts.models import User

def create_test_data():
    # Создаем или получаем категорию
    category, created = Category.objects.get_or_create(
        name='Фрукты',
        defaults={'description': 'Свежие фрукты'}
    )
    
    # Создаем или получаем пользователя-мастера
    master, created = User.objects.get_or_create(
        username='master_test',
        defaults={
            'email': 'master@test.com',
            'role': 'master',
            'first_name': 'Тестовый',
            'last_name': 'Мастер'
        }
    )
    
    # Тестовые товары
    test_products = [
        {
            'name': 'Яблоки красные',
            'description': 'Свежие красные яблоки высшего качества',
            'volume': '1000',
            'package_type': 'Сетка',
            'quantity_in_package': 10,
            'price_per_unit': 15.50,
            'price_per_package': 150.00,
            'price': 15.50,
            'stock': 100
        },
        {
            'name': 'Бананы',
            'description': 'Спелые бананы из Эквадора',
            'volume': '150',
            'package_type': 'Связка',
            'quantity_in_package': 6,
            'price_per_unit': 8.00,
            'price_per_package': 48.00,
            'price': 8.00,
            'stock': 50
        },
        {
            'name': 'Апельсины',
            'description': 'Сочные апельсины из Испании',
            'volume': '200',
            'package_type': 'Коробка',
            'quantity_in_package': 20,
            'price_per_unit': 12.00,
            'price_per_package': 240.00,
            'price': 12.00,
            'stock': 75
        },
        {
            'name': 'Виноград',
            'description': 'Сладкий виноград без косточек',
            'volume': '500',
            'package_type': 'Лоток',
            'quantity_in_package': 5,
            'price_per_unit': 25.00,
            'price_per_package': 125.00,
            'price': 25.00,
            'stock': 30
        },
        {
            'name': 'Клубника',
            'description': 'Свежая клубника отборная',
            'volume': '250',
            'package_type': 'Контейнер',
            'quantity_in_package': 1,
            'price_per_unit': 80.00,
            'price_per_package': 80.00,
            'price': 80.00,
            'stock': 20
        }
    ]
    
    for product_data in test_products:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            master=master,
            defaults={
                **product_data,
                'category': category
            }
        )
        if created:
            print(f"Создан товар: {product.name}")
        else:
            print(f"Товар уже существует: {product.name}")
    
    print(f"\nВсего товаров в базе: {Product.objects.count()}")
    print(f"Категорий: {Category.objects.count()}")

if __name__ == '__main__':
    create_test_data()
