from django.test import TestCase
from django.urls import resolve, reverse

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        root = resolve('/')
        self.assertEqual(root.view_name, 'lists:index')
    
    def test_home_page_returns_correct_html(self):
        url = reverse('lists:index')
        response = self.client.get(url)
        body = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertInHTML('<title>To-Do lists</title>', body)
        self.assertTrue(body.startswith('<html>'))
        self.assertTrue(body.endswith('</html>'))
