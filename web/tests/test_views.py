from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import datetime

from api.models import Manga

class TestSingleViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse("index")
        self.help_needed_url = reverse("help_needed")
        self.search_url = reverse("search")
        self.contrib_url = reverse("contrib")
        self.docs_url = reverse("docs")

    def test_index_GET(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/index.html")

    def test_help_needed_GET(self):
        response = self.client.get(self.help_needed_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/help.html")

    def test_search_GET(self):
        response = self.client.get(self.search_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/search.html")

    def test_contrib_GET(self):
        response = self.client.get(self.contrib_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/contrib.html")

    def test_docs_GET(self):
        response = self.client.get(self.docs_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/api.html")

class TestMangaViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.manga = Manga.objects.create(
            name="Berserk",
            romaji="Berserk",
            description="Berserk manga",
            status="RELEASING",
            start_date=datetime.now()
        )
        self.user = User.objects.create(
            username="BobbyBadBoi",
            email="bobby@badboi.com"
        )
        self.user.set_password("bobbyisabadboi101")
        self.user.save()

    def test_manga_GET_with_correct_id(self):
        response = self.client.get(reverse("manga", args=[self.manga.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/detail.html")

    def test_manga_GET_with_incorrect_id(self):
        response = self.client.get(reverse("manga", args=[100]))
        self.assertEquals(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    def test_manga_widget_GET_with_correct_id(self):
        response = self.client.get(reverse("widget", args=[self.manga.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/widget.svg")

    def test_manga_widget_GET_with_incorrect_id(self):
        response = self.client.get(reverse("widget", args=[100]))
        self.assertEquals(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    def test_new_manga_GET(self):
        self.client.login(username="BobbyBadBoi", password="bobbyisabadboi101")
        response = self.client.get(reverse("new_manga"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/create.html")

    def test_new_manga_GET_no_login(self):
        response = self.client.get(reverse("new_manga"))
        self.assertEquals(response.status_code, 302)

    def test_all_manga_GET(self):
        response = self.client.get(reverse("all_manga"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/all.html")

    def test_all_manga_releasing_GET(self):
        response = self.client.get(reverse("all_manga_releasing"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/all.html")

    def test_all_manga_completed_GET(self):
        response = self.client.get(reverse("all_manga_completed"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/all.html")

class TestAccountViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="BobbyBadBoi",
            email="bobby@badboi.com"
        )
        self.user.set_password("bobbyisabadboi101")
        self.user.save()

    def test_user_GET(self):
        response = self.client.get(reverse("user", args=["BobbyBadBoi"]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/user.html")

    def test_user_GET_no_user_found(self):
        response = self.client.get(reverse("user", args=["BobbyNotABadBoi"]))
        self.assertEquals(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")