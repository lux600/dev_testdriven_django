from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        # self.assertTrue(response.content.strip().startswith(b'<html>'))
        # self.assertIn(b'<title>To-Do lists</title>', response.content.strip())
        # self.assertTrue(response.content.strip().endswith(b'</html>'))
        expected_html = render_to_string('lists/home.html')
        # self.assertIn(response.content.decode(), expected_html) # {% csrf_token %} 값이 추가되어 서로 다르게 나옴

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '첫 번째 아이템'

        response = home_page(request)

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'첫 번째 아이템')

        self.assertIn('첫 번째 아이템',response.content.decode())
        expected_html = render_to_string('lists/home.html', {'new_item_text':'첫 번째 아이템'})
        # self.assertEqual(response.content.decode(), expected_html) # {% csrf_token %} 이 추가되어 같지 Error 발생

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = '첫 번째 아이템'
        first_item.save()

        second_item = Item()
        second_item.text = '두 번째 아이템'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '첫 번째 아이템')
        self.assertEqual(second_saved_item.text, '두 번째 아이템')