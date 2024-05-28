from django.test import TestCase, Client
from django.urls import reverse

class MainViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')
        self.assertContains(response, 'Суші-бар Акамедзутсу')

    def test_about_view(self):
        response = self.client.get(reverse('main:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/about.html')
        self.assertContains(response, 'О нас')

    def test_info_view(self):
        response = self.client.get(reverse('main:info'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/info.html')
        self.assertContains(response, 'Номера телефонів')