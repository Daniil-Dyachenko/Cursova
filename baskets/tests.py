from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from sushi.models import Products, Categories
from users.models import User
from baskets.models import Basket

class TestBasketAdd(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Categories.objects.create(name='Test Category', slug='test-category')
        self.product = Products.objects.create(name='Test Product', price=100.00, slug='test-product', category=self.category)
        self.client.login(username='testuser', password='testpassword')

    def test_basket_add(self):
        response = self.client.post(reverse('basket:basket_add', kwargs={'product_slug': self.product.slug}),
                                    HTTP_REFERER='/')

        self.assertEqual(response.status_code, 302)

        basket = Basket.objects.filter(user=self.user, product=self.product)
        self.assertTrue(basket.exists())

        self.assertEqual(basket.first().quantity, 1)

class TestBasketChange(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Categories.objects.create(name='Test Category', slug='test-category')
        self.product = Products.objects.create(name='Test Product', price=100.00, slug='test-product', category=self.category)
        self.basket = Basket.objects.create(user=self.user, product=self.product, quantity=1)
        self.client.login(username='testuser', password='testpassword')

    def test_basket_increment(self):
        response = self.client.post(reverse('basket:basket_change'), {'basket_id': self.basket.id, 'increment': True})

        self.assertEqual(response.status_code, 302)

        self.basket.refresh_from_db()
        self.assertEqual(self.basket.quantity, 2)

    def test_basket_decrement(self):
        self.basket.quantity = 2
        self.basket.save()

        response = self.client.post(reverse('basket:basket_change'), {'basket_id': self.basket.id, 'decrement': True})

        self.assertEqual(response.status_code, 302)

        self.basket.refresh_from_db()
        self.assertEqual(self.basket.quantity, 1)

    def test_basket_decrement_not_below_one(self):
        response = self.client.post(reverse('basket:basket_change'), {'basket_id': self.basket.id, 'decrement': True})

        self.assertEqual(response.status_code, 302)

        self.basket.refresh_from_db()
        self.assertEqual(self.basket.quantity, 1)

class TestBasketRemove(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser1', password='testpassword1')
        self.category = Categories.objects.create(name='Test Category', slug='test-category')
        self.product = Products.objects.create(name='Test Product', price=100.00, slug='test-product', category=self.category)
        self.basket = Basket.objects.create(user=self.user, product=self.product, quantity=1)
        self.client.login(username='testuser1', password='testpassword1')

    def test_basket_remove(self):
        response = self.client.post(reverse('basket:basket_remove', kwargs={'basket_id': self.basket.id}),
                                    HTTP_REFERER='/')

        self.assertEqual(response.status_code, 302)

        basket_exists = Basket.objects.filter(id=self.basket.id).exists()
        self.assertFalse(basket_exists)
