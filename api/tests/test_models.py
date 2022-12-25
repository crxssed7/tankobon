from django.test import TestCase
from django.utils.timezone import datetime

from api.models import Manga, Volume, Edition


class TestMangaModel(TestCase):
    # TODO: THIS NEEDS MORE WORK.
    # def test_manga_saves_images(self):
    #     manga = Manga.objects.create(
    #         name="Manga Image",
    #         romaji="Manga Image",
    #         description="Manga Image manga",
    #         status="RELEASING",
    #         start_date=datetime.now(),
    #         poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx108556-NHjkz0BNJhLx.jpg",
    #         banner_url="https://s4.anilist.co/file/anilistcdn/media/manga/banner/108556-iCiPfU0GU4OM.jpg"
    #     )
    #     self.assertEquals(manga.poster_file.url, "/media/posters/manga-image_poster.jpeg")
    #     self.assertEquals(manga.banner_file.url, "/media/banners/manga-image_banner.jpeg")
    #     manga.poster_file.delete()
    #     manga.banner_file.delete()

    def test_manga_converts_to_string(self):
        manga = Manga.objects.create(
            name="SPY x FAMILY",
            romaji="SPY x FAMILY",
            description="SPY x FAMILY manga",
            status="RELEASING",
            start_date=datetime.now(),
        )
        self.assertEquals(str(manga), "SPY x FAMILY")


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
            name="Berserk",
            romaji="Berserk",
            description="Berserk",
            status="RELEASING",
            start_date=datetime.now(),
        )
        self.edition = Edition.objects.create(name="Deluxe Edition ", manga=self.manga)

    def test_edition_converts_to_string(self):
        self.assertEquals(str(self.edition), "Berserk: Deluxe Edition")

    def test_edition_correctly_formats_name(self):
        self.assertEquals(str(self.edition.name), "deluxe")
