import os
import shutil

from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.utils.timezone import datetime

from api.models import Manga, Volume, Edition, Language

from tankobon.settings import BASE_DIR


@override_settings(MEDIA_ROOT=str(BASE_DIR / "test_media"))
class TestMangaModel(TestCase):
    def tearDown(self):
        if os.path.exists(str(BASE_DIR / "test_media")):
            shutil.rmtree(str(BASE_DIR / "test_media"))

    def test_manga_saves_images(self):
        manga = Manga.objects.create(
            name="Manga Image",
            romaji="Manga Image",
            description="Manga Image manga",
            status="RELEASING",
            start_date=datetime.now(),
            poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx108556-NHjkz0BNJhLx.jpg",
            banner_url="https://s4.anilist.co/file/anilistcdn/media/manga/banner/108556-iCiPfU0GU4OM.jpg"
        )
        self.assertEquals(manga.poster_file.url, "/media/posters/manga-image/poster.jpeg")
        self.assertEquals(manga.banner_file.url, "/media/heroes/manga-image/hero.jpeg")
        manga.delete()


    def test_manga_converts_to_string(self):
        manga = Manga.objects.create(
            name="SPY x FAMILY",
            romaji="SPY x FAMILY",
            description="SPY x FAMILY manga",
            status="RELEASING",
            start_date=datetime.now(),
        )
        self.assertEquals(str(manga), "SPY x FAMILY")


    def test_manga_poster_only_allows_certain_domains(self):
        invalid_image = Manga(
            name="SPY x FAMILY",
            romaji="SPY x FAMILY",
            description="SPY x FAMILY manga",
            status="RELEASING",
            start_date=datetime.now(),
            poster_url="https://example.com/images/"
        )
        valid_image = Manga(
            name="SPY x FAMILY",
            romaji="SPY x FAMILY",
            description="SPY x FAMILY manga",
            status="RELEASING",
            start_date=datetime.now(),
            poster_url="https://s4.anilist.co/"
        )
        with self.assertRaises(ValidationError):
            invalid_image.full_clean()
        self.assertRaisesMessage(ValidationError, "The image must be from one of the trusted sites. Learn more about this on the contribution guidelines.", invalid_image.full_clean)
        # Prove that we have valid domains
        valid_image.full_clean()


    def test_manga_banner_only_allows_certain_domains(self):
        invalid_image = Manga(
            name="SPY x FAMILY",
            romaji="SPY x FAMILY",
            description="SPY x FAMILY manga",
            status="RELEASING",
            start_date=datetime.now(),
            banner_url="https://example.com/images/"
        )
        valid_image = Manga(
            name="SPY x FAMILY",
            romaji="SPY x FAMILY",
            description="SPY x FAMILY manga",
            status="RELEASING",
            start_date=datetime.now(),
            banner_url="https://s4.anilist.co/"
        )
        with self.assertRaises(ValidationError):
            invalid_image.full_clean()
        self.assertRaisesMessage(ValidationError, "The image must be from one of the trusted sites. Learn more about this on the contribution guidelines.", invalid_image.full_clean)
        # Prove that we have valid domains
        valid_image.full_clean()

    def test_manga_save_creates_japanese_edition(self):
        Language.objects.create(name="Japanese", code="JP")
        manga = Manga.objects.create(
            name="SPY x FAMILY",
            romaji="SPY x FAMILY",
            description="SPY x FAMILY manga",
            status="RELEASING",
            start_date=datetime.now(),
        )
        # Throws exception if not found
        Edition.objects.get(manga=manga, name="standard japanese", language=Language.japanese())


@override_settings(MEDIA_ROOT=str(BASE_DIR / "test_media"))
class TestVolumeModel(TestCase):
    def tearDown(self):
        if os.path.exists(str(BASE_DIR / "test_media")):
            shutil.rmtree(str(BASE_DIR / "test_media"))

    def setUp(self):
        self.manga = Manga.objects.create(
            name="Volume Image",
            romaji="Demon Slayer",
            description="Demon Slayer manga",
            status="RELEASING",
            start_date=datetime.now(),
        )
        self.edition = Edition.objects.first()
        self.volume = Volume.objects.create(absolute_number=0, manga=self.manga)
        self.volume_nontankobon = Volume.objects.create(
            absolute_number=-1, manga=self.manga
        )

    def test_volume_converts_to_string(self):
        self.assertEquals(str(self.volume), "Volume Image Volume 0")

    def test_volume_converts_to_string_nontankobon(self):
        self.assertEquals(str(self.volume_nontankobon), "Volume Image Non-tankobon")

    def test_volume_saves_images(self):
        volume = Volume.objects.create(
            absolute_number=0,
            manga=self.manga,
            edition=self.edition,
            poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx108556-NHjkz0BNJhLx.jpg",
        )
        self.assertEquals(volume.poster_file.url, "/media/posters/volume-image/volumes/standard-japanese/volume_0_poster.jpeg")
        volume.delete()

    def test_volume_poster_only_allows_certain_domains(self):
        invalid_image = Volume(
            absolute_number=99,
            manga=self.manga,
            edition=self.edition,
            chapters="Chapter 1",
            poster_url="https://static.wikia.nocookie.net/"
        )
        valid_image = Volume(
            absolute_number=100,
            manga=self.manga,
            edition=self.edition,
            chapters="Chapter 1",
            poster_url="https://static.wikia.nocookie.net/random/images/"
        )
        with self.assertRaises(ValidationError):
            invalid_image.full_clean()
        self.assertRaisesMessage(ValidationError, "The image must be from one of the trusted sites. Learn more about this on the contribution guidelines.", invalid_image.full_clean)
        # Prove that we have valid domains
        valid_image.full_clean()


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
