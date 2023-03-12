from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import datetime

from api.extras.stats import Statistics
from api.models import Manga, Volume, Edition, Collection, Genre


class TestStatistics(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="BobbyBadBoi", email="bobby@badboi.com"
        )
        shounen = Genre.objects.create(name="Shounen")
        shoujo = Genre.objects.create(name="Shoujo")

        shounen_manga = Manga.objects.create(
            name="MANGA",
            romaji="MANGA",
            description="Manga manga",
            status="RELEASING",
            start_date=datetime.now()
        )
        shounen_manga_edition = Edition.objects.last()
        shounen_manga.genres.set([shounen])

        shounen_volume_1 = Volume.objects.create(
            absolute_number=1,
            manga=shounen_manga,
            edition=shounen_manga_edition,
            chapters="Chapter 1"
        )
        shounen_volume_2 = Volume.objects.create(
            absolute_number=2,
            manga=shounen_manga,
            edition=shounen_manga_edition,
            chapters="Chapter 1"
        )
        shounen_volume_3 = Volume.objects.create(
            absolute_number=3,
            manga=shounen_manga,
            edition=shounen_manga_edition,
            chapters="Chapter 1"
        )
        shounen_volume_4 = Volume.objects.create(
            absolute_number=4,
            manga=shounen_manga,
            edition=shounen_manga_edition,
            chapters="Chapter 1"
        )

        Collection.objects.create(
            user=self.user,
            volume=shounen_volume_1,
            collected_at="2023-03-12"
        )
        Collection.objects.create(
            user=self.user,
            volume=shounen_volume_2,
            collected_at="2023-04-12"
        )
        Collection.objects.create(
            user=self.user,
            volume=shounen_volume_3,
            collected_at="2023-05-12"
        )

        shoujo_manga = Manga.objects.create(
            name="MANGA 2",
            romaji="MANGA 2",
            description="Manga 2 manga",
            status="RELEASING",
            start_date=datetime.now()
        )
        shoujo_manga_edition = Edition.objects.last()
        shoujo_manga.genres.set([shoujo])

        shoujo_volume_1 = Volume.objects.create(
            absolute_number=1,
            manga=shoujo_manga,
            edition=shoujo_manga_edition,
            chapters="Chapter 1"
        )
        shoujo_volume_2 = Volume.objects.create(
            absolute_number=2,
            manga=shoujo_manga,
            edition=shoujo_manga_edition,
            chapters="Chapter 1"
        )

        Collection.objects.create(
            user=self.user,
            volume=shoujo_volume_1,
            collected_at="2023-03-12"
        )
        Collection.objects.create(
            user=self.user,
            volume=shoujo_volume_2,
            collected_at="2023-04-12"
        )

    def test_calculates_public_stats(self):
        stats = Statistics(user=self.user).public()
        self.assertEquals(5, stats["volume_count"])
        self.assertEquals({"Apr 2023": 2, "Mar 2023": 2, "May 2023": 1}, stats["monthly_collected"])
        self.assertEquals({"Josei": 0, "Seinen": 0, "Shoujo": 2, "Shounen": 3}, stats["demographs"])
