from django.shortcuts import render, redirect
from .models import Product
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})

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
