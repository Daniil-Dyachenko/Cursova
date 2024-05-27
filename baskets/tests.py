from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from sushi.models import Products, Categories
from users.models import User
from baskets.models import Basket

# class TestBasketAdd(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.category = Categories.objects.create(name='Test Category', slug='test-category')  # Створіть тестову категорію
#         self.product = Products.objects.create(name='Test Product', price=100.00, slug='test-product', category=self.category)  # Вкажіть категорію при створенні продукту
#         self.client.login(username='testuser', password='testpassword')
#
#     def test_basket_add(self):
#         # Додайте заголовок HTTP_REFERER до запиту
#         response = self.client.post(reverse('basket:basket_add', kwargs={'product_slug': self.product.slug}),
#                                     HTTP_REFERER='/')
#
#         # Перевірте, чи є код відповіді 302 (перенаправлення після успішного додавання товару до кошика)
#         self.assertEqual(response.status_code, 302)
#
#         # Перевірте, чи товар було додано до кошика
#         basket = Basket.objects.filter(user=self.user, product=self.product)
#         self.assertTrue(basket.exists())
#
#         # Перевірте, чи кількість товару в кошику стала 1
#         self.assertEqual(basket.first().quantity, 1)

# class TestBasketChange(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.category = Categories.objects.create(name='Test Category', slug='test-category')  # Створіть тестову категорію
#         self.product = Products.objects.create(name='Test Product', price=100.00, slug='test-product', category=self.category)  # Вкажіть категорію при створенні продукту
#         self.basket = Basket.objects.create(user=self.user, product=self.product, quantity=1)  # Створіть корзину з одним товаром
#         self.client.login(username='testuser', password='testpassword')
#
#     def test_basket_increment(self):
#         response = self.client.post(reverse('basket:basket_change'), {'basket_id': self.basket.id, 'increment': True})
#
#         # Перевірте, чи є код відповіді 302 (перенаправлення після успішної зміни товару у кошику)
#         self.assertEqual(response.status_code, 302)
#
#         # Перевірте, чи кількість товару в кошику збільшилася на 1
#         self.basket.refresh_from_db()
#         self.assertEqual(self.basket.quantity, 2)
#
#     def test_basket_decrement(self):
#         # Збільшіть кількість товару в кошику, щоб мати можливість зменшити
#         self.basket.quantity = 2
#         self.basket.save()
#
#         response = self.client.post(reverse('basket:basket_change'), {'basket_id': self.basket.id, 'decrement': True})
#
#         # Перевірте, чи є код відповіді 302 (перенаправлення після успішної зміни товару у кошику)
#         self.assertEqual(response.status_code, 302)
#
#         # Перевірте, чи кількість товару в кошику зменшилася на 1
#         self.basket.refresh_from_db()
#         self.assertEqual(self.basket.quantity, 1)
#
#     def test_basket_decrement_not_below_one(self):
#         response = self.client.post(reverse('basket:basket_change'), {'basket_id': self.basket.id, 'decrement': True})
#
#         # Перевірте, чи є код відповіді 302 (перенаправлення після успішної зміни товару у кошику)
#         self.assertEqual(response.status_code, 302)
#
#         # Перевірте, що кількість товару в кошику залишилася 1 і не зменшилася нижче 1
#         self.basket.refresh_from_db()
#         self.assertEqual(self.basket.quantity, 1)
#
# # Запустіть цей клас тестів для перевірки функціональності зміни кількості товару у кошику

class TestBasketRemove(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser1', password='testpassword1')
        self.category = Categories.objects.create(name='Test Category', slug='test-category')  # Створіть тестову категорію
        self.product = Products.objects.create(name='Test Product', price=100.00, slug='test-product', category=self.category)  # Вкажіть категорію при створенні продукту
        self.basket = Basket.objects.create(user=self.user, product=self.product, quantity=1)  # Створіть корзину з одним товаром
        self.client.login(username='testuser1', password='testpassword1')

    def test_basket_remove(self):
        # Додайте заголовок HTTP_REFERER до запиту
        response = self.client.post(reverse('basket:basket_remove', kwargs={'basket_id': self.basket.id}),
                                    HTTP_REFERER='/')

        # Перевірте, чи є код відповіді 302 (перенаправлення після успішного видалення товару з кошика)
        self.assertEqual(response.status_code, 302)

        # Перевірте, чи товар було видалено з кошика
        basket_exists = Basket.objects.filter(id=self.basket.id).exists()
        self.assertFalse(basket_exists)

# Запустіть цей клас тестів для перевірки функціональності видалення товару з кошика