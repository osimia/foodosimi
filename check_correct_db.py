#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Добавляем путь к проекту
sys.path.append(str(Path(__file__).parent))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fruitsite.settings')
django.setup()

from django.db import connection

def check_database():
    print("=== ПРОВЕРКА БАЗЫ ДАННЫХ ===")
    
    # Проверяем подключение
    try:
        with connection.cursor() as cursor:
            # Получаем информацию о базе данных
            cursor.execute("SELECT current_database(), current_user, version();")
            db_info = cursor.fetchone()
            print(f"База данных: {db_info[0]}")
            print(f"Пользователь: {db_info[1]}")
            print(f"Версия PostgreSQL: {db_info[2]}")
            print()
            
            # Получаем список всех таблиц
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            
            print(f"=== НАЙДЕНО ТАБЛИЦ: {len(tables)} ===")
            if tables:
                for table in tables:
                    print(f"- {table[0]}")
            else:
                print("НЕТ ТАБЛИЦ в схеме 'public'")
            print()
            
            # Проверяем наличие таблицы django_migrations
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'django_migrations'
                );
            """)
            has_migrations = cursor.fetchone()[0]
            
            if has_migrations:
                cursor.execute("SELECT COUNT(*) FROM django_migrations;")
                migrations_count = cursor.fetchone()[0]
                print(f"Таблица django_migrations существует, записей: {migrations_count}")
                
                # Показываем последние миграции
                cursor.execute("""
                    SELECT app, name, applied 
                    FROM django_migrations 
                    ORDER BY applied DESC 
                    LIMIT 10;
                """)
                recent_migrations = cursor.fetchall()
                if recent_migrations:
                    print("\nПоследние миграции:")
                    for migration in recent_migrations:
                        print(f"  {migration[0]}.{migration[1]} - {migration[2]}")
            else:
                print("Таблица django_migrations НЕ СУЩЕСТВУЕТ")
                
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")

if __name__ == "__main__":
    check_database()
