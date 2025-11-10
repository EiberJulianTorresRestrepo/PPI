from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('questions/', views.questions, name='questions'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
]
