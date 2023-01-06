from django.test import TestCase
from django.urls import reverse
from lists.models import Item, List

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        url = reverse('lists:index')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'lists/index.html')
    
class ListViewTest(TestCase):
    def test_uses_list_template(self):
        new_list = List.objects.create()
        url = reverse('lists:view_list', args=[new_list.id])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

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
        new_list = List.objects.first()
        new_url = reverse('lists:view_list', args=[new_list.id])
        self.assertRedirects(response, new_url)

class NewItemViewTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        throwaway_list = List.objects.create()
        correct_list = List.objects.create()

        url = reverse('lists:add_item', args=[correct_list.id])
        self.client.post(url, data={'item_text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)
    
    def test_redirects_to_list_view(self):
        throwaway_list = List.objects.create()
        correct_list = List.objects.create()

        url = reverse('lists:add_item', args=[correct_list.id])
        response = self.client.post(url, data={'item_text': 'A new item for an existing list'})

        new_url = reverse('lists:view_list', args=[correct_list.id])
        self.assertRedirects(response, new_url)
    
    def test_passes_correct_list_to_template(self):
        throwaway_list = List.objects.create()
        correct_list = List.objects.create()

        url = reverse('lists:view_list', args=[correct_list.id])
        response = self.client.get(url)
        self.assertEqual(response.context['list'], correct_list)


class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_list = List()
        first_list.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = first_list
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = first_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, first_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, first_list)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, first_list)
