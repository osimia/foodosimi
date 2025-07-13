from django import template
from cart.models import CartItem
from cart.views import get_cart_owner_info

register = template.Library()

@register.simple_tag(takes_context=True)
def cart_items_count(context):
    """Возвращает количество товаров в корзине"""
    request = context['request']
    
    try:
        owner_filter, _ = get_cart_owner_info(request)
        cart_items = CartItem.objects.filter(**owner_filter)
        return sum(item.quantity for item in cart_items)
    except:
        return 0
