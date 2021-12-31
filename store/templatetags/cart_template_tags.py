from django import template
from store.models import Order

register = template.Library()

@register.filter
def cart_product_count(user):
    if user.is_authenticated:
        qnty = Order.objects.filter(user=user, ordered=False)
        if qnty.exists():
            return qnty[0].products.count()
    return 0