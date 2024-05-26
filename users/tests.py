from django.test import TestCase
from django.urls import reverse
from users.models import User

class UserRegistrationTest(TestCase):
    def test_registration_view(self):
        """
        Перевіряємо, чи сторінка реєстрації відображається правильно
        """
        response = self.client.get(reverse('user:registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')
    def test_user_registration(self):
        """
        Перевіряємо, чи користувач може зареєструватися з правильними даними
        """
        user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(reverse('users:registration'), user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_invalid_user_registration(self):
        """
        Перевіряємо, що система відхиляє невірні дані під час реєстрації
        """
        user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'email': 'invalidemail',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(reverse('users:registration'), user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser').exists())