from django.core.management.base import BaseCommand
from products.models import Category


class Command(BaseCommand):
    help = 'Удаляет старые дефолтные категории и создает новые глобальные'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Удалить старые категории без товаров',
        )

    def handle(self, *args, **options):
        # Старые категории для удаления
        old_categories = [
            'Национальная одежда',
            'Украшения', 
            'Аксессуары',
            'Обувь',
            'Домашний декор',
        ]
        
        if options['clean']:
            # Удаляем старые категории, которые не используются
            deleted_count = 0
            for cat_name in old_categories:
                try:
                    category = Category.objects.get(name=cat_name)
                    # Проверяем, есть ли товары в этой категории
                    if category.product_set.count() == 0:
                        category.delete()
                        deleted_count += 1
                        self.stdout.write(f'Удалена категория: {cat_name}')
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Категория "{cat_name}" содержит товары и не была удалена'
                            )
                        )
                except Category.DoesNotExist:
                    pass
            
            self.stdout.write(
                self.style.SUCCESS(f'Удалено {deleted_count} неиспользуемых категорий')
            )
        
        # Создаем новые глобальные категории
        new_categories = [
            ('Фрукты и овощи', 'Свежие фрукты, овощи и зелень'),
            ('Молочные продукты', 'Молоко, сыр, йогурт и другие молочные продукты'), 
            ('Мясо и птица', 'Свежее мясо, птица и мясные изделия'),
            ('Хлебобулочные изделия', 'Хлеб, выпечка и кондитерские изделия'),
            ('Напитки', 'Соки, вода, чай и другие напитки'),
        ]
        
        created_count = 0
        for name, description in new_categories:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={
                    'description': description,
                    'is_global': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'Создана глобальная категория: {name}')
            else:
                # Обновляем существующую категорию
                category.is_global = True
                category.description = description
                category.save()
                self.stdout.write(f'Обновлена категория: {name}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Создано {created_count} новых глобальных категорий')
        )
