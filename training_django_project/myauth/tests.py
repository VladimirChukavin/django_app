import json

from django.test import TestCase
from django.urls import reverse


class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        response = self.client.get(reverse("myauth:get_cookies"))
        self.assertContains(response, "Value of cookie one")
        # self.assertContains(response, "qwerty")


class FooBarTestCase(TestCase):
    def test_foo_bar_view(self) -> None:
        response = self.client.get(reverse("myauth:foo_bar"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")

        expected_data = {"foo": 12, "bar": True}
        # received_data = json.loads(response.content)
        # self.assertEqual(received_data, expected_data)
        self.assertJSONEqual(response.content, expected_data)
