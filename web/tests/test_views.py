from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import datetime

from api.models import Manga, Volume, Edition, Genre


class TestSingleViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse("index")
        self.help_needed_url = reverse("help_needed")
        self.search_url = reverse("search")
        self.contrib_url = reverse("contrib")

    def test_index_GET(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/index.html")

    def test_help_needed_GET(self):
        response = self.client.get(self.help_needed_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/help.html")

    def test_search_GET(self):
        Genre.objects.create(name="Shounen")
        Genre.objects.create(name="Shoujo")
        Genre.objects.create(name="Seinen")
        Genre.objects.create(name="Josei")
        response = self.client.get(self.search_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/manga/manga_search.html")

    def test_contrib_GET(self):
        response = self.client.get(self.contrib_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/contrib.html")


class TestMangaViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.manga = Manga.objects.create(
            name="Berserk",
            romaji="Berserk",
            description="Berserk manga",
            status="RELEASING",
            start_date=datetime.now(),
        )
        self.user = User.objects.create(
            username="BobbyBadBoi", email="bobby@badboi.com"
        )
        self.user.set_password("bobbyisabadboi101")
        self.user.save()

    def test_manga_GET_with_correct_id(self):
        response = self.client.get(reverse("manga", args=[self.manga.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/manga/manga_detail.html")

    def test_manga_GET_with_incorrect_id(self):
        response = self.client.get(reverse("manga", args=[100]))
        self.assertEquals(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    def test_manga_widget_GET_with_correct_id(self):
        response = self.client.get(reverse("widget", args=[self.manga.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/manga/manga_widget.svg")

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
        self.assertTemplateUsed(response, "web/manga/manga_list.html")

    def test_edit_manga_GET(self):
        self.client.login(username="BobbyBadBoi", password="bobbyisabadboi101")
        response = self.client.get(reverse("edit_manga", args=[self.manga.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/manga/manga_edit.html")

    def test_edit_manga_GET_no_login(self):
        response = self.client.get(reverse("edit_manga", args=[self.manga.id]))
        self.assertEquals(response.status_code, 302)

    def test_edit_manga_locked_GET(self):
        locked_record = Manga.objects.create(
            name="Locked Record",
            romaji="Locked Record",
            description="Locked Record",
            status="RELEASING",
            start_date=datetime.now(),
            locked=True,
        )
        self.client.login(username="BobbyBadBoi", password="bobbyisabadboi101")
        response = self.client.get(reverse("edit_manga", args=[locked_record.id]))
        self.assertEquals(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    def test_edit_manga_does_not_exist_GET(self):
        self.client.login(username="BobbyBadBoi", password="bobbyisabadboi101")
        response = self.client.get(reverse("edit_manga", args=[43565743]))
        self.assertEquals(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")


class TestVolumeViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.manga = Manga.objects.create(
            name="Berserk",
            romaji="Berserk",
            description="Berserk manga",
            status="RELEASING",
            start_date=datetime.now(),
        )
        self.edition = Edition.objects.first()
        self.volume = Volume.objects.create(
            absolute_number=0, manga=self.manga, edition=self.edition
        )
        self.user = User.objects.create(
            username="BobbyBadBoi", email="bobby@badboi.com"
        )
        self.user.set_password("bobbyisabadboi101")
        self.user.save()

    def test_edit_volume_GET(self):
        self.client.login(username="BobbyBadBoi", password="bobbyisabadboi101")
        response = self.client.get(reverse("edit_volume", args=[self.manga.id, 0]) + "?edition=standard")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/volume/volume_edit.html")

    def test_edit_volume_GET_no_login(self):
        response = self.client.get(reverse("edit_volume", args=[self.manga.id, 0]) + "?edition=standard")
        self.assertEquals(response.status_code, 302)

    def test_edit_volume_locked_GET(self):
        locked_record = Volume.objects.create(
            absolute_number=1, manga=self.manga, locked=True
        )
        self.client.login(username="BobbyBadBoi", password="bobbyisabadboi101")
        response = self.client.get(reverse("edit_volume", args=[self.manga.id, 1]) + "?edition=standard")
        self.assertEquals(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    def test_edit_volume_does_not_exist_GET(self):
        self.client.login(username="BobbyBadBoi", password="bobbyisabadboi101")
        response = self.client.get(reverse("edit_volume", args=[self.manga.id, -1]) + "?edition=standard")
        self.assertEquals(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    def test_edit_non_tankobon_volume_GET(self):
        non_tankobon = Volume.objects.create(
            absolute_number=-1, manga=self.manga, edition=self.edition
        )
        self.client.login(username="BobbyBadBoi", password="bobbyisabadboi101")
        response = self.client.get(reverse("edit_volume", args=[self.manga.id, -1]) + "?edition=standard")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/volume/volume_edit.html")

    def test_new_volume_GET(self):
        self.client.login(username="BobbyBadBoi", password="bobbyisabadboi101")
        response = self.client.get(reverse("new_volume", args=[self.manga.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/create.html")

    def test_new_volume_GET_no_login(self):
        response = self.client.get(reverse("new_volume", args=[self.manga.id]))
        self.assertEquals(response.status_code, 302)

    def test_new_volume_manga_is_locked_GET(self):
        locked_record = Manga.objects.create(
            name="Locked Record",
            romaji="Locked Record",
            description="Locked Record",
            status="RELEASING",
            start_date=datetime.now(),
            locked=True,
        )
        self.client.login(username="BobbyBadBoi", password="bobbyisabadboi101")
        response = self.client.get(reverse("new_volume", args=[locked_record.id]))
        self.assertEquals(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")


class TestAccountViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="BobbyBadBoi", email="bobby@badboi.com"
        )
        self.user.set_password("bobbyisabadboi101")
        self.user.save()

    def test_user_GET(self):
        response = self.client.get(reverse("user", args=["BobbyBadBoi"]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "web/users/user_detail.html")

    def test_user_GET_no_user_found(self):
        response = self.client.get(reverse("user", args=["BobbyNotABadBoi"]))
        self.assertEquals(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
