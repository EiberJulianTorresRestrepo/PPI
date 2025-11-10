from django.test import TestCase, RequestFactory
from store.models import Category, Product
from store.cart import Cart
from store.services import add_to_cart_service, remove_from_cart_service

class CartTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(name='Jewelry', slug='jewelry')
        self.product = Product.objects.create(
            category=self.category,
            name='Aretes',
            slug='aretes',
            description='Test product',
            price='150.00'
        )

    def test_add_and_total(self):
        request = self.factory.get('/')
        # attach a real session object from the test client
        request.session = self.client.session
        cart = Cart(request)
        cart.add(self.product, quantity=2)
        items = list(cart)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['quantity'], 2)
        self.assertEqual(float(cart.get_total_price()), 300.0)

    def test_service_add_remove(self):
        request = self.factory.get('/')
        request.session = self.client.session
        # add via service
        add_to_cart_service(request, product_id=self.product.id, quantity=1, update=False)
        cart = Cart(request)
        self.assertEqual(float(cart.get_total_price()), 150.0)
        # remove via service
        remove_from_cart_service(request, product_id=self.product.id)
        cart = Cart(request)
        self.assertEqual(len(list(cart)), 0)
