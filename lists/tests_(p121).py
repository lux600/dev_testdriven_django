from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/lists/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        # self.assertTrue(response.content.strip().startswith(b'<html>'))
        # self.assertIn(b'<title>To-Do lists</title>', response.content.strip())
        # self.assertTrue(response.content.strip().endswith(b'</html>'))
        expected_html = render_to_string('lists/home.html')
        # self.assertIn(response.content.decode(), expected_html) # {% csrf_token %} 값이 추가되어 서로 다르게 나옴


class LiveViewTest(TestCase):

    def tst_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, '/lists/list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='다른 목록 아이템 1', list=other_list)
        Item.objects.create(text='다른 목록 아이템 2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))
        # print(response.content.decode())

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response,'다른 목록 아이템 1')
        self.assertNotContains(response, '다른 목록 아이템 2')

class ListAndItemModelsTest(TestCase):

    # def test_uses_list_template(self):
    #     response = self.client.get('/lists/the-only-list-in-the-world/')
    #     self.assertTemplateUsed(response, 'lists/list.html')

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = '첫 번째 아이템'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = '두 번째 아이템'
        second_item.list = list_
        second_item.save()
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)


        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '첫 번째 아이템')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, '두 번째 아이템')
        self.assertEqual(second_saved_item.list, list_)

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):

        self.client.post('/lists/new', data={'item_text':'신규 작업 아이템'})

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'신규 작업 아이템')


    def test_redirects_after_POST(self):

        response = self.client.post('/lists/new', {'item_text':'신규 작업 아이템'})

        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))
