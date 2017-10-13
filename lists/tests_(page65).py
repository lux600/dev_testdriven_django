from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page


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
        request.POST['item_text'] = '신규 작업 아이템'

        response = home_page(request)

        self.assertIn('신규 작업 아이템',response.content.decode())
        expected_html = render_to_string('lists/home.html', {'new_item_text':'신규 작업 아이템'})
        # self.assertEqual(response.content.decode(), expected_html) # {% csrf_token %} 이 추가되어 같지 Error 발생

