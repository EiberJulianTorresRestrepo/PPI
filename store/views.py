from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Product
from .forms import ContactForm, CartAddProductForm
from .cart import Cart
from django.core.mail import send_mail
from django.conf import settings

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
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart_detail.html', {'cart': cart})

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

