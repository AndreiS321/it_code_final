from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.test import TestCase, Client
from django.urls import reverse

from profiles import models
from profiles.factories import ProfileFactory, PASSWORD


# Create your tests here.
class UnauthorizedTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login(self):
        user = ProfileFactory.create()

        resp = self.client.post(reverse("profiles:login"),
                                {"username": user.username,
                                 "password": PASSWORD})
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_register(self):
        user = ProfileFactory.build()

        resp = self.client.post(reverse("profiles:registration"),
                                {"username": user.username,
                                 "password1": PASSWORD,
                                 "password2": PASSWORD, })
        user_db = models.Profile.objects.filter(username=user.username).first()
        self.assertIsNotNone(user_db)

    def test_detail(self):
        user = ProfileFactory.create()

        resp = self.client.get(reverse("profiles:profile",
                                       kwargs={"pk": user.pk}))
        self.assertEqual(resp.status_code, 200)


class AuthorizedTests(TestCase):
    def setUp(self) -> None:
        self.user = ProfileFactory.create()
        self.client = Client()
        self.client.login(username=self.user.username, password=PASSWORD)

        self.user2 = ProfileFactory.create()
        self.client2 = Client()
        self.client2.login(username=self.user2.username, password=PASSWORD)

        self.unauthorized_client = Client()

    def test_update(self):
        new_description = "Test3"
        resp = self.client.post(reverse("profiles:update",
                                        kwargs={"pk": self.user.pk}),
                                {"username": self.user.username,
                                 "profile_pic": "",
                                 "description": new_description})

        user_db = models.Profile.objects.filter(pk=self.user.pk).first()
        self.assertEqual(user_db.username, self.user.username)
        self.assertEqual(user_db.description, new_description)

    def test_update_failed(self):
        new_description = "Test3"
        resp = self.client2.post(reverse("profiles:update",
                                         kwargs={"pk": self.user.pk}),
                                 {"username": self.user.username,
                                  "profile_pic": "",
                                  "description": new_description})

        user_db = models.Profile.objects.filter(pk=self.user.pk).first()
        self.assertEqual(user_db.username, self.user.username)
        self.assertEqual(user_db.description, self.user.description)

    def test_update_unauthorized(self):
        new_description = "Test3"
        resp = self.unauthorized_client.post(
            reverse("profiles:update",
                    kwargs={"pk": self.user.pk}),
            {"username": self.user.username,
             "profile_pic": "",
             "description": new_description})
        user_db = models.Profile.objects.filter(pk=self.user.pk).first()
        self.assertEqual(user_db.username, self.user.username)
        self.assertEqual(user_db.description, self.user.description)

    def test_delete(self):
        user = ProfileFactory.create()
        client = Client()
        client.login(username=user.username, password=PASSWORD)
        resp = client.post(reverse("profiles:delete",
                                   kwargs={"pk": user.pk}))

        user_db = models.Profile.objects.filter(pk=user.pk).first()
        self.assertIsNone(user_db)

    def test_delete_failed(self):
        user = ProfileFactory.create()
        client = Client()
        client.login(username=user.username, password=PASSWORD)
        resp = self.client.post(reverse("profiles:delete",
                                        kwargs={"pk": user.pk}))

        user_db = models.Profile.objects.filter(pk=user.pk).first()
        self.assertIsNotNone(user_db)

    def test_delete_unauthorized(self):
        user = ProfileFactory.create()
        resp = self.unauthorized_client.post(reverse("profiles:delete",
                                                     kwargs={"pk": user.pk}))

        user_db = models.Profile.objects.filter(pk=user.pk).first()
        self.assertIsNotNone(user_db)

    def test_change_password(self):
        user = ProfileFactory.create()
        client = Client()
        client.login(username=user.username, password=PASSWORD)
        resp = client.post(reverse("profiles:change_password",
                                   kwargs={"pk": user.pk}),
                           {
                               "old_password": PASSWORD,
                               "new_password1": PASSWORD + "1",
                               "new_password2": PASSWORD + "1", })
        user_db = models.Profile.objects.filter(pk=user.pk).first()
        self.assertTrue(check_password(PASSWORD + "1", user_db.password))

    def test_change_password_failed(self):
        user = ProfileFactory.create()
        client = Client()
        client.login(username=user.username, password=PASSWORD)
        resp = self.client.post(reverse("profiles:change_password",
                                        kwargs={"pk": user.pk}),
                                {
                                    "old_password": PASSWORD,
                                    "new_password1": PASSWORD + "1",
                                    "new_password2": PASSWORD + "1", })
        user_db = models.Profile.objects.filter(pk=user.pk).first()
        self.assertFalse(check_password(PASSWORD + "1", user_db.password))

    def test_change_password_unauthorized(self):
        user = ProfileFactory.create()
        resp = self.unauthorized_client.post(reverse(
            "profiles:change_password",
            kwargs={"pk": user.pk}),
            {
                "old_password": PASSWORD,
                "new_password1": PASSWORD + "1",
                "new_password2": PASSWORD + "1", })

        user_db = models.Profile.objects.filter(pk=user.pk).first()
        self.assertFalse(check_password(PASSWORD + "1", user_db.password))

    def test_logout(self):
        resp = self.client.get(reverse("profiles:logout"))
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
