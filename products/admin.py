# fruitsite/products/admin.py
from django.contrib import admin
from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_global', 'created_by', 'created_at']
    list_filter = ['is_global', 'created_by', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description')
        }),
        ('Настройки доступа', {
            'fields': ('is_global', 'created_by'),
            'description': 'Глобальные категории доступны всем пользователям'
        }),
        ('Метаданные', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 5

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'master', 'volume', 'package_type', 
        'quantity_in_package', 'price_per_unit', 'price_per_package', 
        'stock', 'created_at'
    ]
    list_filter = ['category', 'master', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('master', 'category', 'name', 'description')
        }),
        ('Характеристики упаковки', {
            'fields': ('volume', 'package_type', 'quantity_in_package'),
            'classes': ('collapse',)
        }),
        ('Ценообразование', {
            'fields': ('price_per_unit', 'price_per_package', 'price', 'old_price'),
            'classes': ('collapse',)
        }),
        ('Наличие', {
            'fields': ('stock',),
            'classes': ('collapse',)
        }),
        ('Метаданные', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']
    list_filter = ['product__category']
