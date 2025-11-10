from django.test import TestCase, Client
from django.urls import reverse

class PaymentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.payment_url = reverse('process_payment')

    def test_payment_with_credit_card(self):
        response = self.client.post(self.payment_url, {
            'payment_method': 'credit_card',
            'amount': '100',
            'card_number': '1234567812345678',
            'expiry_date': '2025-12',
            'cvv': '123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'status': 'success',
            'message': 'Pago procesado correctamente.'
        })

    def test_payment_with_missing_card_details(self):
        response = self.client.post(self.payment_url, {
            'payment_method': 'credit_card',
            'amount': '100'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'status': 'error',
            'message': 'Faltan datos de la tarjeta.'
        })

    def test_payment_with_paypal(self):
        response = self.client.post(self.payment_url, {
            'payment_method': 'paypal',
            'amount': '100'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'status': 'success',
            'message': 'Pago procesado correctamente.'
        })

    def test_invalid_method(self):
        response = self.client.get(self.payment_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'status': 'error',
            'message': 'Método no permitido.'
        })