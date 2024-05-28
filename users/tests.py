from django.test import TestCase,Client
from django.urls import reverse
from users.models import User
from django.contrib.auth import get_user_model

class UserRegistrationTest(TestCase):
    def test_registration_view(self):

        response = self.client.get(reverse('user:registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')
    def test_user_registration(self):

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


class TestUserLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login(self):
        response = self.client.post(reverse('user:login'), {'username': 'testuser', 'password': 'testpassword'},
                                    follow=True)
        user = self.client.session['_auth_user_id']
        self.assertEqual(user, str(self.user.pk))

        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_with_incorrect_credentials(self):
        response = self.client.post(reverse('user:login'), {'username': 'wronguser', 'password': 'wrongpassword'})

        self.assertEqual(response.status_code, 200)

        self.assertFalse(response.context['user'].is_authenticated)

class TestLogout(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_logout(self):
        response = self.client.get(reverse('users:logout'))

        self.assertEqual(response.status_code, 302)

        self.assertFalse('_auth_user_id' in self.client.session)

        self.assertRedirects(response, reverse('main:index'))