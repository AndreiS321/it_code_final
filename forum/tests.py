from django.test import TestCase, Client
from django.urls import reverse

from forum import models
from forum.factories import CategoryFactory, ThemeFactory, ThemeMessageFactory
from profiles.factories import PASSWORD, AdminFactory, ProfileFactory


# Create your tests here.
class UnauthorizedTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_categories(self):
        resp = self.client.get(reverse("forum:categories"))
        self.assertEqual(resp.status_code, 200)

    def test_themes(self):
        category = CategoryFactory.create()
        resp = self.client.get(
            reverse("forum:themes",
                    kwargs={"category_pk": category.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_theme(self):
        theme = ThemeFactory.create()
        resp = self.client.get(
            reverse("forum:theme",
                    kwargs={"pk": theme.pk}))
        self.assertEqual(resp.status_code, 200)


class CategoriesTests(TestCase):
    def setUp(self) -> None:
        self.user = ProfileFactory.create()
        self.client = Client()
        self.client.login(username=self.user.username,
                          password=PASSWORD)

        self.admin = AdminFactory.create()
        self.admin_client = Client()
        self.admin_client.login(username=self.admin.username,
                                password=PASSWORD)

        self.unauthorized_client = Client()

    def test_category_create(self):
        category = CategoryFactory.build()
        resp = self.admin_client.post(
            reverse("forum:category_create"),
            {"name": category.name})
        category_db = models.Category.objects.filter(
            name=category.name).first()
        self.assertEqual(category_db.name, category.name)

    def test_category_create_unauthorized(self):
        category = CategoryFactory.build()
        resp = self.unauthorized_client.post(
            reverse("forum:category_create"),
            {"name": category.name})
        category_db = models.Category.objects.filter(
            name=category.name).first()
        self.assertIsNone(category_db)

    def test_category_create_not_staff(self):
        category = CategoryFactory.build()
        resp = self.client.post(
            reverse("forum:category_create"),
            {"name": category.name})
        category_db = models.Category.objects.filter(
            name=category.name).first()
        self.assertIsNone(category_db)

    def test_category_delete(self):
        category = CategoryFactory.create()
        resp = self.admin_client.post(
            reverse("forum:category_delete",
                    kwargs={"pk": category.pk}))
        category_db = models.Category.objects.filter(
            name=category.name).first()
        self.assertIsNone(category_db)

    def test_category_delete_unauthorized(self):
        category = CategoryFactory.create()
        resp = self.unauthorized_client.post(
            reverse("forum:category_delete",
                    kwargs={"pk": category.pk}))
        category_db = models.Category.objects.filter(
            name=category.name).first()
        self.assertIsNotNone(category_db)

    def test_category_delete_not_staff(self):
        category = CategoryFactory.create()
        resp = self.client.post(
            reverse("forum:category_delete",
                    kwargs={"pk": category.pk}))
        category_db = models.Category.objects.filter(
            name=category.name).first()
        self.assertIsNotNone(category_db)


class ThemesTests(TestCase):
    def setUp(self) -> None:
        self.user = ProfileFactory.create()
        self.client = Client()
        self.client.login(username=self.user.username,
                          password=PASSWORD)

        self.admin = AdminFactory.create()
        self.admin_client = Client()
        self.admin_client.login(username=self.admin.username,
                                password=PASSWORD)

        self.unauthorized_client = Client()

    def test_theme_create(self):
        category = CategoryFactory.create()
        theme = ThemeFactory.build(category=category)
        resp = self.admin_client.post(
            reverse("forum:theme_create",
                    kwargs={"category_pk": category.pk}),
            {"name": theme.name})
        theme_db = models.Theme.objects.filter(
            name=theme.name).first()
        self.assertEqual(theme_db.name, theme.name)

    def test_theme_create_unauthorized(self):
        category = CategoryFactory.create()
        theme = ThemeFactory.build(category=category)
        resp = self.unauthorized_client.post(
            reverse("forum:theme_create",
                    kwargs={"category_pk": category.pk}),
            {"name": theme.name})
        theme_db = models.Theme.objects.filter(
            name=theme.name).first()
        self.assertIsNone(theme_db)

    def test_theme_create_not_staff(self):
        category = CategoryFactory.create()
        theme = ThemeFactory.build(category=category)
        resp = self.client.post(
            reverse("forum:theme_create",
                    kwargs={"category_pk": category.pk}),
            {"name": theme.name})
        theme_db = models.Theme.objects.filter(
            name=theme.name).first()
        self.assertEqual(theme_db.name, theme.name)

    def test_theme_delete(self):
        category = CategoryFactory.create()
        theme = ThemeFactory.create(category=category)
        resp = self.admin_client.post(
            reverse("forum:theme_delete",
                    kwargs={"category_pk": category.pk,
                            "pk": theme.pk}))
        theme_db = models.Theme.objects.filter(
            pk=theme.pk).first()
        self.assertIsNone(theme_db)

    def test_theme_delete_unauthorized(self):
        category = CategoryFactory.create()
        theme = ThemeFactory.create(category=category)
        resp = self.unauthorized_client.post(
            reverse("forum:theme_delete",
                    kwargs={"category_pk": category.pk,
                            "pk": theme.pk}))
        theme_db = models.Theme.objects.filter(
            pk=theme.pk).first()
        self.assertIsNotNone(theme_db)

    def test_theme_delete_not_staff(self):
        category = CategoryFactory.create()
        theme = ThemeFactory.create(category=category, creator=self.user)
        resp = self.client.post(
            reverse("forum:theme_delete",
                    kwargs={"category_pk": category.pk,
                            "pk": theme.pk}))
        theme_db = models.Theme.objects.filter(
            pk=theme.pk).first()
        self.assertIsNone(theme_db)

    def test_theme_delete_not_staff_failed(self):
        category = CategoryFactory.create()
        theme = ThemeFactory.create(category=category)
        resp = self.client.post(
            reverse("forum:theme_delete",
                    kwargs={"category_pk": category.pk,
                            "pk": theme.pk}))
        theme_db = models.Theme.objects.filter(
            pk=theme.pk).first()
        self.assertIsNotNone(theme_db)

    def test_theme_message_create(self):
        theme = ThemeFactory.create()
        msg = ThemeMessageFactory.build(theme=theme)
        resp = self.admin_client.post(
            reverse("forum:create_message"),
            {"text": msg.text,
             "theme_pk": theme.pk})
        msg_db = models.ThemeMessage.objects.filter(
            theme__pk=msg.theme.pk).first()
        self.assertEqual(msg_db.text, msg.text)

    def test_theme_message_create_unauthorized(self):
        category = CategoryFactory.create()
        theme = ThemeFactory.build(category=category)
        resp = self.unauthorized_client.post(
            reverse("forum:theme_create",
                    kwargs={"category_pk": category.pk}),
            {"name": theme.name})
        theme_db = models.Theme.objects.filter(
            name=theme.name).first()
        self.assertIsNone(theme_db)
