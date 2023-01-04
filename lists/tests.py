from django.test import TestCase
from django.urls import resolve, reverse

class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        url = reverse('lists:index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/index.html')
