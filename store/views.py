from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Product
from .forms import ContactForm, CartAddProductForm
from .cart import Cart
from .services import add_to_cart_service, remove_from_cart_service, get_cart_summary
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

# ... (home, shop, about, questions, contact views remain the same) ...
def home(request):
    return render(request, 'home.html')

def shop(request):
    products = Product.objects.all()
    cart_product_form = CartAddProductForm()
    return render(request, 'shop.html', {'products': products, 'cart_product_form': cart_product_form})

def about(request):
    return render(request, 'about.html')

def questions(request):
    return render(request, 'questions.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Optional: send email
            # send_mail(
            #     f'Message from {name}',
            #     message,
            #     email,
            #     ['your_email@example.com'], # Replace with your email
            # )
            
            return redirect('home') # Redirect after POST
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


@require_POST
def add_to_cart(request, product_id):
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        add_to_cart_service(request, product_id=product_id, quantity=cd['quantity'], update=cd['update'])
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    remove_from_cart_service(request, product_id=product_id)
    return redirect('cart_detail')

def cart_detail(request):
    context = get_cart_summary(request)
    # attach update form to items
    for item in context['items']:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart_detail.html', {'cart': context['cart']})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    cart_product_form = CartAddProductForm()

    # Get previous and next products
    products = list(Product.objects.all())
    product_index = products.index(product)

    previous_product = products[product_index - 1] if product_index > 0 else None
    next_product = products[product_index + 1] if product_index < len(products) - 1 else None

    return render(request, 'product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'previous_product': previous_product,
        'next_product': next_product
    })

def process_payment(request):
    from .cart import Cart
    cart = Cart(request)
    total_amount = cart.get_total_price()
    if request.method == 'POST':
        logger.info('Solicitud POST recibida en process_payment')
        payment_method = request.POST.get('payment_method')
        amount = total_amount
        logger.info(f'Método de pago: {payment_method}, Monto: {amount}')

        # Simulate payment processing
        if payment_method in ['credit_card', 'debit_card']:
            card_number = request.POST.get('card_number')
            expiry_date = request.POST.get('expiry_date')
            cvv = request.POST.get('cvv')
            logger.info(f'Detalles de la tarjeta: {card_number}, {expiry_date}, {cvv}')

            if not (card_number and expiry_date and cvv):
                logger.error('Faltan detalles de la tarjeta')
                return render(request, 'payment_form.html', {
                    'error': 'Faltan datos de la tarjeta.',
                    'total_amount': total_amount
                })

        elif payment_method == 'paypal':
            logger.info('Procesando pago con PayPal')

        # Simulate successful payment
        logger.info('Pago procesado exitosamente')
        return redirect('payment_success')

    return render(request, 'payment_form.html', {'total_amount': total_amount})

def payment_success(request):
    return render(request, 'payment_success.html')

