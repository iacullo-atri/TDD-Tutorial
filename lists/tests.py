from django.test import TestCase
from django.urls import resolve, reverse

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        url = reverse('lists:index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/index.html')
    
    def test_can_save_a_POST_request(self):
        url = reverse('lists:index')
        response = self.client.post(url, data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'lists/index.html')
