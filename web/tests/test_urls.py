from django.contrib.auth.views import LoginView, LogoutView
from django.test import SimpleTestCase
from django.urls import reverse, resolve

from web.views.manga.views import (
    new_manga,
    all_manga,
    all_manga_completed,
    all_manga_releasing,
    edit_manga,
    MangaDetailView,
    MangaWidgetView,
)
from web.views.volume.views import edit_volume, new_volume
from web.views.singles.views import (
    IndexView,
    contrib,
    docs,
    HelpNeededView,
    SearchResultsView,
    SignUpView,
)
from web.views.users.views import UserDetailView


class TestMiscUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse("index")
        self.assertEquals(resolve(url).func.__name__, IndexView.as_view().__name__)

    def test_contrib_url_is_resolved(self):
        url = reverse("contrib")
        self.assertEquals(resolve(url).func, contrib)

    def test_docs_url_is_resolved(self):
        url = reverse("docs")
        self.assertEquals(resolve(url).func, docs)

    def test_help_needed_url_is_resolved(self):
        url = reverse("help_needed")
        self.assertEquals(resolve(url).func.__name__, HelpNeededView.as_view().__name__)


class TestMangaUrls(SimpleTestCase):
    def test_search_url_is_resolved(self):
        url = reverse("search")
        self.assertEquals(
            resolve(url).func.__name__, SearchResultsView.as_view().__name__
        )

    def test_new_manga_url_is_resolved(self):
        url = reverse("new_manga")
        self.assertEquals(resolve(url).func, new_manga)

    def test_all_manga_url_is_resolved(self):
        url = reverse("all_manga")
        self.assertEquals(resolve(url).func, all_manga)

    def test_all_manga_completed_url_is_resolved(self):
        url = reverse("all_manga_completed")
        self.assertEquals(resolve(url).func, all_manga_completed)

    def test_all_manga_releasing_url_is_resolved(self):
        url = reverse("all_manga_releasing")
        self.assertEquals(resolve(url).func, all_manga_releasing)

    def test_manga_url_is_resolved(self):
        url = reverse("manga", args=[1])
        self.assertEquals(
            resolve(url).func.__name__, MangaDetailView.as_view().__name__
        )

    def test_widget_url_is_resolved(self):
        url = reverse("widget", args=[1])
        self.assertEquals(
            resolve(url).func.__name__, MangaWidgetView.as_view().__name__
        )

    def test_edit_manga_url_is_resolved(self):
        url = reverse("edit_manga", args=[1])
        self.assertEquals(resolve(url).func, edit_manga)


class TestVolumeUrls(SimpleTestCase):
    def test_edit_volume_url_is_resolved(self):
        url = reverse("edit_volume", args=[1, 1])
        self.assertEquals(resolve(url).func, edit_volume)

    def test_edit_non_tankobon_volume_url_is_resolved(self):
        url = reverse("edit_volume", args=[1, -1])
        self.assertEquals(resolve(url).func, edit_volume)

    def test_new_volume_url_is_resolved(self):
        url = reverse("new_volume", args=[1])
        self.assertEquals(resolve(url).func, new_volume)


class TestAccountUrls(SimpleTestCase):
    def test_login_url_is_resolved(self):
        url = reverse("login")
        self.assertEquals(resolve(url).func.__name__, LoginView.as_view().__name__)

    def test_logout_url_is_resolved(self):
        url = reverse("logout")
        self.assertEquals(resolve(url).func.__name__, LogoutView.as_view().__name__)

    def test_signup_url_is_resolved(self):
        url = reverse("signup")
        self.assertEquals(resolve(url).func.__name__, SignUpView.as_view().__name__)

    def test_user_url_is_resolved(self):
        url = reverse("user", args=["some-user"])
        self.assertEquals(resolve(url).func.__name__, UserDetailView.as_view().__name__)
