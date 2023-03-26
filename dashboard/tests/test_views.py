from django.contrib.auth.models import User
from django.test import TestCase, Client, modify_settings, RequestFactory
from django.urls import reverse
from django.utils.timezone import datetime

from api.models import Manga, Volume, Edition, Genre, Collection

from dashboard.views import LibraryView

from web.forms import CollectionForm


@modify_settings(MIDDLEWARE={
    "remove": "tankobon.middleware.SqlPrintMiddleware",
})
class TestLibraryViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="BobbyBadBoi", email="bobby@badboi.com"
        )
        self.user.set_password("bobbyisabadboi101")
        self.user.save()

        manga_1 = Manga.objects.create(
            name="Test",
            romaji="Test",
            description="Test",
            status="RELEASING",
            start_date=datetime.now()
        )
        vol_1 = Volume.objects.create(
            absolute_number=1,
            manga=manga_1,
            edition=manga_1.edition_set.first()
        )
        self.col_1 = Collection.objects.create(
            user=self.user,
            volume=vol_1,
            edition=vol_1.edition
        )

        manga_2 = Manga.objects.create(
            name="This is a manga",
            romaji="123",
            description="123",
            status="RELEASING",
            start_date=datetime.now()
        )
        vol_2 = Volume.objects.create(
            absolute_number=1,
            manga=manga_2,
            edition=manga_2.edition_set.first()
        )
        self.col_2 = Collection.objects.create(
            user=self.user,
            volume=vol_2,
            edition=vol_2.edition
        )

        manga_3 = Manga.objects.create(
            name="This is a manga",
            romaji="123",
            description="123",
            status="RELEASING",
            start_date=datetime.now()
        )
        self.vol_3 = Volume.objects.create(
            absolute_number=1,
            manga=manga_3,
            edition=manga_3.edition_set.first(),
            isbn="978-4-08-880723-2"
        )

    def test_library_GET(self):
        self.client.login(username="BobbyBadBoi", password="bobbyisabadboi101")
        response = self.client.get(reverse("dashboard"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/library.html")

    def test_library_GET_not_logged_in(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEquals(response.status_code, 302)

    def test_library_context(self):
        factory = RequestFactory()
        request = factory.get(reverse("dashboard"))
        request.user = self.user
        request.htmx = None
        response = LibraryView.as_view()(request)
        self.assertIsInstance(response.context_data, dict)
        self.assertEqual(len(response.context_data["results"]), 2)
        self.assertIsInstance(response.context_data["add_collection_form"], CollectionForm)

    def test_library_search(self):
        factory = RequestFactory()
        request = factory.get(reverse("dashboard") + "?q=Test")
        request.user = self.user
        request.htmx = None
        response = LibraryView.as_view()(request)
        self.assertIsInstance(response.context_data, dict)
        self.assertEqual(response.context_data["query"], "Test")
        self.assertEqual(len(response.context_data["results"]), 1)

    def test_library_templates_htmx(self):
        self.client.login(username="BobbyBadBoi", password="bobbyisabadboi101")
        response = self.client.get(reverse("dashboard"), **{"HTTP_HX-Request": "true"})
        self.assertTemplateUsed(response, "dashboard/_library.html")

    def test_library_POST_no_login(self):
        response = self.client.post(reverse("dashboard"))
        self.assertEquals(response.status_code, 302)

    def test_library_POST_invalid(self):
        self.client.login(username="BobbyBadBoi", password="bobbyisabadboi101")
        response = self.client.post(reverse("dashboard"), data={}, follow=True)
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Could not add this volume to your collection.")

    def test_library_POST_valid(self):
        self.client.login(username="BobbyBadBoi", password="bobbyisabadboi101")
        response = self.client.post(reverse("dashboard"), data={"isbn": "9784088807232", "collected_at": "2023-01-01"}, follow=True)
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Volume was added to your collection.")
        # Raises error if not found
        Collection.objects.get(user=self.user, volume=self.vol_3, edition=self.vol_3.edition)


@modify_settings(MIDDLEWARE={
    "remove": "tankobon.middleware.SqlPrintMiddleware",
})
class TestCollectionViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="BobbyBadBoi", email="bobby@badboi.com"
        )
        self.user.set_password("bobbyisabadboi101")
        self.user.save()

        self.other_user = User.objects.create(
            username="Other", email="other@other.com"
        )
        self.other_user.set_password("topsecret")
        self.other_user.save()

        manga_1 = Manga.objects.create(
            name="Test",
            romaji="Test",
            description="Test",
            status="RELEASING",
            start_date=datetime.now()
        )
        vol_1 = Volume.objects.create(
            absolute_number=1,
            manga=manga_1,
            edition=manga_1.edition_set.first()
        )
        self.col_1 = Collection.objects.create(
            user=self.user,
            volume=vol_1,
            edition=vol_1.edition
        )

    def test_collection_GET(self):
        self.client.login(username="BobbyBadBoi", password="bobbyisabadboi101")
        response = self.client.get(reverse("collection", args=[self.col_1.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/collection.html")

    def test_collection_GET_no_login(self):
        response = self.client.get(reverse("collection", args=[self.col_1.id]))
        self.assertEquals(response.status_code, 404)

    def test_collection_GET_no_access(self):
        self.client.login(username="Other", password="topsecret")
        response = self.client.get(reverse("collection", args=[self.col_1.id]))
        self.assertEquals(response.status_code, 404)

    def test_collection_GET_templates_htmx(self):
        self.client.login(username="BobbyBadBoi", password="bobbyisabadboi101")
        response = self.client.get(reverse("collection", args=[self.col_1.id]), **{"HTTP_HX-Request": "true"})
        self.assertTemplateUsed(response, "dashboard/_collection.html")

    def test_library_POST_success_url(self):
        self.client.login(username="BobbyBadBoi", password="bobbyisabadboi101")
        response = self.client.post(reverse("collection", args=[self.col_1.id]), data={"collected_at": "2023-01-01"})
        self.assertRedirects(response, reverse("collection", args=[self.col_1.id]))

    def test_library_POST_no_access(self):
        self.client.login(username="Other", password="topsecret")
        response = self.client.post(reverse("collection", args=[self.col_1.id]), data={})
        self.assertEquals(response.status_code, 404)

@modify_settings(MIDDLEWARE={
    "remove": "tankobon.middleware.SqlPrintMiddleware",
})
class TestStatisticsViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="BobbyBadBoi", email="bobby@badboi.com"
        )
        self.user.set_password("bobbyisabadboi101")
        self.user.save()

    def test_statistics_GET(self):
        self.client.login(username="BobbyBadBoi", password="bobbyisabadboi101")
        response = self.client.get(reverse("private_stats"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/statistics.html")

    def test_statistics_GET_no_login(self):
        response = self.client.get(reverse("private_stats"))
        self.assertEquals(response.status_code, 302)
