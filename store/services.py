from decimal import Decimal
from .cart import Cart
from .models import Product


def add_to_cart_service(request, product_id, quantity=1, update=False):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add(product=product, quantity=quantity, update_quantity=update)
    return cart


def remove_from_cart_service(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.remove(product)
    return cart


def get_cart_summary(request):
    cart = Cart(request)
    total = cart.get_total_price()
    items = list(cart)
    return {'cart': cart, 'total': total, 'items': items}
