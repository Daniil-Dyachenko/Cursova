from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from sushi.models import Products, Categories
from baskets.models import Basket
from customs.models import Custom, CustomItem

User = get_user_model()

class TestCreateOrder(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Categories.objects.create(name='Test Category', slug='test-category')
        self.product = Products.objects.create(name='Test Product', price=100.00, slug='test-product', category=self.category, quantity=10)
        self.client.login(username='testuser', password='testpassword')
        self.basket = Basket.objects.create(user=self.user, product=self.product, quantity=1)

    def test_create_order(self):
        response = self.client.post(reverse('customs:create_customs'), {
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '0123456789',
            'requires_delivery': '1',
            'delivery_address': 'Test Address',
            'payment_on_get': '0',
        })

        # Перевіряємо код відповіді
        self.assertEqual(response.status_code, 302)

        # Перевіряємо, чи створено замовлення
        self.assertTrue(Custom.objects.filter(user=self.user).exists())

        # Перевіряємо, чи очищено кошик
        self.assertFalse(Basket.objects.filter(user=self.user).exists())