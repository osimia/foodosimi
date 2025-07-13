from django.core.management.base import BaseCommand
from products.models import Category, Product


class Command(BaseCommand):
    help = 'Удаляет все глобальные категории из базы данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Подтверждение удаления глобальных категорий',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    'Эта команда удалит все глобальные категории и обнулит категории у товаров, которые их используют.\n'
                    'Для подтверждения запустите команду с флагом --confirm'
                )
            )
            return

        # Получаем все глобальные категории
        global_categories = Category.objects.filter(is_global=True)
        
        if not global_categories.exists():
            self.stdout.write(
                self.style.SUCCESS('Глобальные категории не найдены.')
            )
            return

        # Показываем какие категории будут удалены
        self.stdout.write('Будут удалены следующие глобальные категории:')
        for category in global_categories:
            self.stdout.write(f'  - {category.name}')

        # Обнуляем категории у товаров, которые используют глобальные категории
        products_with_global_categories = Product.objects.filter(
            category__in=global_categories
        )
        
        if products_with_global_categories.exists():
            count = products_with_global_categories.count()
            products_with_global_categories.update(category=None)
            self.stdout.write(
                self.style.WARNING(
                    f'У {count} товаров была обнулена категория.'
                )
            )

        # Удаляем глобальные категории
        deleted_count = global_categories.count()
        global_categories.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно удалено {deleted_count} глобальных категорий.'
            )
        )
