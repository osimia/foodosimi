#!/usr/bin/env python
import os
import sys
import django

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fruitsite.settings')
django.setup()

from django.db import connection

def check_database_tables():
    """Проверяем все таблицы в базе данных"""
    print("=== ПРОВЕРКА ТАБЛИЦ В БАЗЕ ДАННЫХ ===\n")
    
    with connection.cursor() as cursor:
        # Получаем список всех таблиц
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        
        if tables:
            print(f"Найдено {len(tables)} таблиц:")
            print("-" * 50)
            
            for i, (table_name,) in enumerate(tables, 1):
                print(f"{i:2d}. {table_name}")
                
                # Получаем информацию о колонках для каждой таблицы
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns 
                    WHERE table_name = %s AND table_schema = 'public'
                    ORDER BY ordinal_position;
                """, [table_name])
                
                columns = cursor.fetchall()
                if columns:
                    print(f"    Колонки ({len(columns)}):")
                    for col_name, data_type, is_nullable in columns:
                        nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
                        print(f"      - {col_name} ({data_type}) {nullable}")
                else:
                    print("    Нет колонок")
                print()
        else:
            print("Таблицы не найдены!")
            
        # Проверяем таблицу django_migrations
        print("\n=== ПРОВЕРКА МИГРАЦИЙ ===")
        cursor.execute("""
            SELECT app, name, applied 
            FROM django_migrations 
            ORDER BY applied DESC
            LIMIT 20;
        """)
        
        migrations = cursor.fetchall()
        if migrations:
            print(f"Последние {len(migrations)} миграций:")
            print("-" * 60)
            for app, name, applied in migrations:
                print(f"{applied} | {app} | {name}")
        else:
            print("Миграции не найдены!")

if __name__ == '__main__':
    try:
        check_database_tables()
    except Exception as e:
        print(f"Ошибка при проверке базы данных: {e}")
        import traceback
        traceback.print_exc()
