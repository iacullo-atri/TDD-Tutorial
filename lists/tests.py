from django.test import TestCase
from django.urls import resolve

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        root = resolve('/')
        self.assertEqual(root.view_name, 'lists:index')
    