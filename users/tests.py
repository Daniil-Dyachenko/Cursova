from django.test import TestCase,Client
from django.urls import reverse
from users.models import User
from django.contrib.auth import get_user_model

# class UserRegistrationTest(TestCase):
#     # def test_registration_view(self):
#     #     """
#     #     Перевіряємо, чи сторінка реєстрації відображається правильно
#     #     """
#     #     response = self.client.get(reverse('user:registration'))
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertTemplateUsed(response, 'users/registration.html')
#     def test_user_registration(self):
#         """
#         Перевіряємо, чи користувач може зареєструватися з правильними даними
#         """
#         user_data = {
#             'first_name': 'Test',
#             'last_name': 'User',
#             'username': 'testuser',
#             'email': 'test@example.com',
#             'password1': 'testpassword123',
#             'password2': 'testpassword123',
#         }
#         response = self.client.post(reverse('users:registration'), user_data)
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(User.objects.filter(username='testuser').exists())
#
#     def test_invalid_user_registration(self):
#         """
#         Перевіряємо, що система відхиляє невірні дані під час реєстрації
#         """
#         user_data = {
#             'first_name': 'Test',
#             'last_name': 'User',
#             'username': 'testuser',
#             'email': 'invalidemail',
#             'password1': 'testpassword123',
#             'password2': 'testpassword123',
#         }
#         response = self.client.post(reverse('users:registration'), user_data)
#         self.assertEqual(response.status_code, 200)
#         self.assertFalse(User.objects.filter(username='testuser').exists())


# class TestUserLogin(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#
#     def test_login(self):
#         response = self.client.post(reverse('user:login'), {'username': 'testuser', 'password': 'testpassword'},
#                                     follow=True)
#         # Перевірте, чи є користувач авторизований
#         user = self.client.session['_auth_user_id']
#         self.assertEqual(user, str(self.user.pk))
#
#         # Перевірте, чи є код відповіді 200
#         self.assertEqual(response.status_code, 200)
#
#         # Перевірте, чи є користувач вже авторизований
#         self.assertTrue(response.context['user'].is_authenticated)

    # def test_login_with_incorrect_credentials(self):
    #     response = self.client.post(reverse('user:login'), {'username': 'wronguser', 'password': 'wrongpassword'})
    #
    #     # Перевірте, чи є код відповіді 200
    #     self.assertEqual(response.status_code, 200)
    #
    #     # Перевірте, чи є користувач вже авторизований
    #     self.assertFalse(response.context['user'].is_authenticated)

class TestLogout(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_logout(self):
        # Виконуємо вихід користувача
        response = self.client.get(reverse('users:logout'))

        # Перевіряємо код відповіді після виходу (повинно бути перенаправлення на головну сторінку)
        self.assertEqual(response.status_code, 302)

        # Перевіряємо, чи користувач справді вийшов
        self.assertFalse('_auth_user_id' in self.client.session)

        # Перевіряємо перенаправлення на головну сторінку
        self.assertRedirects(response, reverse('main:index'))

        # # Перевіряємо, чи повідомлення про успішний вихід не з'явилося безпосередньо після виходу
        # response = self.client.get(reverse('main:index'))
        # messages_list = list(response.context['messages'])
        # self.assertFalse(messages_list)
        #
        # # Повторно переходимо на головну сторінку, щоб перевірити, чи з'явилося повідомлення
        # response = self.client.get(reverse('main:index'))
        #
        # # Перевіряємо наявність повідомлення про успішний вихід
        # messages_list = list(response.context['messages'])
        # self.assertTrue(
        #     any(str(message) == 'testuser, Ви успішно вийшли із свого аккаунту' for message in messages_list))