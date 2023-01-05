from django.test import TestCase
from django.urls import resolve, reverse
from lists.models import Item

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        url = reverse('lists:index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/index.html')
    
    def test_can_save_a_POST_request(self):
        url = reverse('lists:index')
        data={'item_text': 'A new list item'}
        self.client.post(url, data)

        self.assertEqual(Item.objects.count(), 1)
        saved_item = Item.objects.first()
        self.assertEqual(saved_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        url = reverse('lists:index')
        data={'item_text': 'A new list item'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
    
    def test_only_saves_items_when_necessary(self):
        url = reverse('lists:index')
        self.client.get(url)
        self.assertEqual(Item.objects.count(), 0)
    
    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        url = reverse('lists:index')
        response = self.client.get(url)
        body = response.content.decode()

        self.assertIn('itemey 1', body)
        self.assertIn('itemey 2', body)


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
