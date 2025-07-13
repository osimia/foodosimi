from django.core.management.base import BaseCommand
from products.models import Category


class Command(BaseCommand):
    help = 'Преобразует существующие категории в глобальные'

    def handle(self, *args, **options):
        # Находим все категории без created_by (старые категории)
        old_categories = Category.objects.filter(created_by__isnull=True)
        
        if not old_categories.exists():
            self.stdout.write(
                self.style.SUCCESS('Нет категорий для преобразования.')
            )
            return
        
        # Делаем их глобальными
        updated_count = old_categories.update(is_global=True)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно преобразовано {updated_count} категорий в глобальные.'
            )
        )
        
        # Выводим список преобразованных категорий
        for category in old_categories:
            self.stdout.write(f'  - {category.name}')
