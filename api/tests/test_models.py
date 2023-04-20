import os
import shutil

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.utils.timezone import datetime

from api.models import Manga, Volume, Edition, Language, Genre, Collection

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
        self.volume = Volume.objects.create(absolute_number=0, manga=self.manga, edition=self.edition)
        self.volume_nontankobon = Volume.objects.create(
            absolute_number=-1, manga=self.manga, edition=self.edition
        )

    def test_volume_converts_to_string(self):
        self.assertEquals(str(self.volume), "Volume Image Volume 0")

    def test_volume_converts_to_string_nontankobon(self):
        self.assertEquals(str(self.volume_nontankobon), "Volume Image Non-tankobon")

    def test_volume_saves_images(self):
        volume = Volume.objects.create(
            absolute_number=1,
            manga=self.manga,
            edition=self.edition,
            poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx108556-NHjkz0BNJhLx.jpg",
        )
        self.assertEquals(volume.poster_file.url, "/media/posters/volume-image/volumes/standard-japanese/volume_1_poster.jpeg")
        volume.delete()

    def test_volume_save_formats_isbn(self):
        volume = Volume.objects.create(
            absolute_number=1,
            manga=self.manga,
            edition=self.edition,
            isbn="978-4-08-880723-2"
        )
        self.assertEquals(volume.isbn, "9784088807232")

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

    def test_volume_when_is_oneshot_and_does_not_have_volumes(self):
        manga = Manga.objects.create(
            name="Oneshot",
            romaji="Oneshot",
            description="OneShot",
            status="RELEASING",
            start_date=datetime.now(),
            is_oneshot=True
        )
        edition = manga.edition_set.first()
        # Does not raise an error
        Volume.objects.create(absolute_number=0, manga=manga, edition=edition)

    def test_volume_when_is_oneshot_and_has_volume(self):
        manga = Manga.objects.create(
            name="Oneshot",
            romaji="Oneshot",
            description="OneShot",
            status="RELEASING",
            start_date=datetime.now(),
            is_oneshot=True
        )
        edition = manga.edition_set.first()
        # Does not raise an error as the edition does not have any volumes at this point
        Volume.objects.create(absolute_number=0, manga=manga, edition=edition)
        with self.assertRaises(ValidationError):
            Volume.objects.create(absolute_number=1, manga=manga, edition=edition)
        with self.assertRaisesMessage(ValidationError, "A oneshot manga can only have one volume."):
            Volume.objects.create(absolute_number=1, manga=manga, edition=edition)

    def test_volume_when_is_oneshot_and_can_be_updated(self):
        manga = Manga.objects.create(
            name="Oneshot",
            romaji="Oneshot",
            description="OneShot",
            status="RELEASING",
            start_date=datetime.now(),
            is_oneshot=True
        )
        edition = manga.edition_set.first()
        volume = Volume.objects.create(absolute_number=0, manga=manga, edition=edition)
        volume.absolute_number = 1
        volume.save()
        self.assertEquals(volume.absolute_number, 1)


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


class TestCollectionModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="BobbyBadBoi", email="bobby@badboi.com"
        )
        self.manga = Manga.objects.create(
            name="Berserk",
            romaji="Berserk",
            description="Berserk",
            status="RELEASING",
            start_date=datetime.now(),
        )
        self.volume = Volume.objects.create(
            absolute_number=1,
            manga=self.manga,
            edition=self.manga.edition_set.first()
        )

    def test_collection_saves_edition_from_volume(self):
        collection = Collection.objects.create(
            user=self.user,
            volume=self.volume,
            collected_at=datetime.now()
        )
        self.assertEquals(collection.edition, self.volume.edition)


class TestLanguageModel(TestCase):
    def test_language_converts_to_string(self):
        lang = Language.objects.create(name="Japanese", code="JP")
        self.assertEquals(str(lang), "Japanese")


class TestGenreModel(TestCase):
    def test_genre_converts_to_string(self):
        genre = Genre.objects.create(name="Comedy")
        self.assertEquals(str(genre), "Comedy")
