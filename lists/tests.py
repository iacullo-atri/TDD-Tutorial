from django.test import TestCase
from django.urls import resolve, reverse
from lists.models import Item

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        url = reverse('lists:index')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'lists/index.html')
    
class ListViewTest(TestCase):
    def test_uses_list_template(self):
        url = reverse('lists:view_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'lists/list.html')

    
    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        url = '/lists/the-only-list-in-the-world/'
        response = self.client.get(url)

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

class NewListViewTest(TestCase):
    def test_can_save_a_POST_request(self):
        url = reverse('lists:new_list')
        self.client.post(url, data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
    
    def test_redirects_after_POST(self):
        url = reverse('lists:new_list')
        response = self.client.post(url, data={'item_text': 'A new list item'})
        self.assertRedirects(response, reverse('lists:view_list'))

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
