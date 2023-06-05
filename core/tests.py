from django.test import TestCase, Client
from django.urls import reverse


# Create your tests here.
class IndexTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_index(self):
        resp = self.client.get(reverse("core:index"))

        self.assertEqual(resp.status_code, 200)
