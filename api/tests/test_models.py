from django.test import TestCase
from django.utils.timezone import datetime

from api.models import Manga, Volume, Edition


class TestMangaModel(TestCase):
    def setUp(self):
        self.manga = Manga.objects.create(
            name="SPY x FAMILY",
            romaji="SPY x FAMILY",
            description="SPY x FAMILY manga",
            status="RELEASING",
            start_date=datetime.now(),
        )

    def test_manga_converts_to_string(self):
        self.assertEquals(str(self.manga), "SPY x FAMILY")


class TestVolumeModel(TestCase):
    def setUp(self):
        self.manga = Manga.objects.create(
            name="Demon Slayer",
            romaji="Demon Slayer",
            description="Demon Slayer manga",
            status="RELEASING",
            start_date=datetime.now(),
        )
        self.volume = Volume.objects.create(absolute_number=0, manga=self.manga)
        self.volume_nontankobon = Volume.objects.create(
            absolute_number=-1, manga=self.manga
        )

    def test_volume_converts_to_string(self):
        self.assertEquals(str(self.volume), "Demon Slayer Volume 0")

    def test_volume_converts_to_string_nontankobon(self):
        self.assertEquals(str(self.volume_nontankobon), "Demon Slayer Non-tankobon")


class TestEditionModel(TestCase):
    def setUp(self):
        self.manga = Manga.objects.create(
            name="Demon Slayer",
            romaji="Demon Slayer",
            description="Demon Slayer manga",
            status="RELEASING",
            start_date=datetime.now(),
        )
        self.edition = Edition.objects.create(name="Standard Edition ", manga=self.manga)
        self.volume = Volume.objects.create(absolute_number=0, manga=self.manga, edition=self.edition)

    def test_edition_converts_to_string(self):
        self.assertEquals(str(self.edition), "Demon Slayer: Standard Edition")

    def test_edition_correctly_formats_name(self):
        self.assertEquals(str(self.edition.name), "standard")