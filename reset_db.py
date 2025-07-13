#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fruitsite.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection

def reset_database():
    """Очистка всех таблиц и данных миграций"""
    with connection.cursor() as cursor:
        # Получаем список всех таблиц
        cursor.execute("""
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public' 
            AND tablename NOT LIKE 'pg_%' 
            AND tablename NOT LIKE 'sql_%'
        """)
        tables = cursor.fetchall()
        
        print(f"Найдено {len(tables)} таблиц для удаления:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Отключаем проверку внешних ключей
        cursor.execute("SET foreign_key_checks = 0;")
        
        # Удаляем все таблицы
        for table in tables:
            table_name = table[0]
            print(f"Удаляем таблицу: {table_name}")
            cursor.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE;')
        
        print("Все таблицы удалены!")

if __name__ == "__main__":
    reset_database()
