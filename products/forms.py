from django import forms
from django.db import models
from .models import Product, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': 'Название категории',
            'description': 'Описание категории',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Описание категории (необязательно)'}),
            'name': forms.TextInput(attrs={'placeholder': 'Введите название категории'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'description', 'volume', 'package_type', 
            'quantity_in_package', 'price_per_unit', 'price_per_package', 
            'price', 'old_price', 'stock'
        ]
        labels = {
            'category': 'Категория',
            'name': 'Наименование продукции',
            'description': 'Описание',
            'volume': 'Объем, г',
            'package_type': 'Вид упаковки',
            'quantity_in_package': 'Количество в упаковке',
            'price_per_unit': 'Цена за единицу',
            'price_per_package': 'Цена за упаковку',
            'price': 'Цена (для совместимости)',
            'old_price': 'Старая цена',
            'stock': 'Количество в наличии',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Показываем только категории, созданные текущим пользователем
        if user:
            available_categories = Category.objects.filter(
                created_by=user
            ).order_by('name')
            self.fields['category'].queryset = available_categories
        else:
            # Если пользователь не передан, показываем пустой queryset
            self.fields['category'].queryset = Category.objects.none()

    def clean_price_per_unit(self):
        price = self.cleaned_data.get('price_per_unit')
        if price is not None and price < 0:
            raise forms.ValidationError('Цена за единицу не может быть отрицательной')
        return price
    
    def clean_price_per_package(self):
        price = self.cleaned_data.get('price_per_package')
        if price is not None and price < 0:
            raise forms.ValidationError('Цена за упаковку не может быть отрицательной')
        return price
    
    def clean_quantity_in_package(self):
        quantity = self.cleaned_data.get('quantity_in_package')
        if quantity is not None and quantity < 1:
            raise forms.ValidationError('Количество в упаковке должно быть больше 0')
        return quantity
    
    def clean(self):
        cleaned_data = super().clean()
        price_per_unit = cleaned_data.get('price_per_unit')
        price_per_package = cleaned_data.get('price_per_package')
        quantity_in_package = cleaned_data.get('quantity_in_package')
        
        # Автоматически рассчитываем цену за упаковку, если она не указана
        if price_per_unit and quantity_in_package and not price_per_package:
            cleaned_data['price_per_package'] = price_per_unit * quantity_in_package
        
        # Синхронизируем старое поле price с price_per_unit для совместимости
        if price_per_unit and not cleaned_data.get('price'):
            cleaned_data['price'] = price_per_unit
        
        return cleaned_data
