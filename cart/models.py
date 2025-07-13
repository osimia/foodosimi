# duzanda/cart/models.py

from django.db import models
from accounts.models import User
from products.models import Product

class CartItem(models.Model):
    UNIT_CHOICES = (
        ('unit', 'За единицу'),
        ('package', 'За упаковку'),
    )
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_type = models.CharField(max_length=10, choices=UNIT_CHOICES, default='unit', verbose_name='Тип единицы')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(buyer__isnull=False) | models.Q(session_key__isnull=False),
                name='cart_item_has_owner'
            )
        ]

    def get_price(self):
        """Возвращает цену в зависимости от типа единицы"""
        if self.unit_type == 'package':
            return self.product.price_per_package
        return self.product.price_per_unit
    
    def get_total_price(self):
        """Возвращает общую стоимость товара"""
        return self.get_price() * self.quantity

    def __str__(self):
        size_str = f" [{self.size}]" if self.size else ""
        unit_display = dict(self.UNIT_CHOICES)[self.unit_type]
        owner = self.buyer.username if self.buyer else f"Session {self.session_key[:8]}..."
        return f"{self.product.name}{size_str} x {self.quantity} ({unit_display}) for {owner}"
