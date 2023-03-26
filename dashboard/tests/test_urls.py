from django.contrib.auth.views import LogoutView
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.views.generic import TemplateView

from dashboard.views import LibraryView, CollectionDetailView, StatisticsView


class TestDashboardUrls(SimpleTestCase):
    def test_dashboard_url_is_resolved(self):
        url = reverse("dashboard")
        self.assertEquals(resolve(url).func.__name__, LibraryView.as_view().__name__)

    def test_collection_url_is_resolved(self):
        url = reverse("collection", args=[1])
        self.assertEquals(resolve(url).func.__name__, CollectionDetailView.as_view().__name__)

    def test_statistics_url_is_resolved(self):
        url = reverse("private_stats")
        self.assertEquals(resolve(url).func.__name__, StatisticsView.as_view().__name__)
