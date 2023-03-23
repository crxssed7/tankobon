import os
import shutil

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.utils.timezone import datetime

from api.models import Volume, Manga

from web.templatetags import utility

from tankobon.settings import BASE_DIR


class UtilityTesterClass:
    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2


@override_settings(MEDIA_ROOT=str(BASE_DIR / "test_media"))
class TestUtilityTags(TestCase):
    def tearDown(self):
        if os.path.exists(str(BASE_DIR / "test_media")):
            shutil.rmtree(str(BASE_DIR / "test_media"))

    def setUp(self):
        self.no_image = Manga.objects.create(
            name="Manga Image",
            romaji="Manga Image",
            description="Manga Image manga",
            status="RELEASING",
            start_date=datetime.now()
        )

    def test_urlparams(self):
        expected_1 = "?greeting=hellothere&response=generalkenobi"
        actual_1 = utility.urlparams(greeting="hellothere", response="generalkenobi")
        self.assertEquals(expected_1, actual_1)
        expected_2 = ""
        actual_2 = utility.urlparams()
        self.assertEquals(expected_2, actual_2)


    def test_capitalize(self):
        value = "hello there My friend"
        expected = "Hello There My Friend"
        actual = utility.capitalize(value)
        self.assertEquals(expected, actual)


    def test_active_tab(self):
        value = "/manga/new/"
        expected_1 = "text-white px-3 py-2 rounded-md text-sm font-medium"
        actual_1 = utility.active_tab(value, "manga")
        self.assertEquals(expected_1, actual_1)
        expected_2 = "text-gray-300 hover:text-white hover:text-white px-3 py-2 rounded-md text-sm font-medium"
        actual_2 = utility.active_tab(value, "test")
        self.assertEquals(expected_2, actual_2)


    def test_poster_url(self):
        manga = Manga.objects.create(
            name="Manga Image",
            romaji="Manga Image",
            description="Manga Image manga",
            status="RELEASING",
            start_date=datetime.now(),
            poster_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx108556-NHjkz0BNJhLx.jpg"
        )
        expected_1 = "/media/posters/manga-image/poster.jpeg"
        actual_1 = utility.poster_url(manga)
        self.assertEquals(expected_1, actual_1)
        expected_2 = ""
        actual_2 = utility.poster_url(self.no_image)
        self.assertEquals(expected_2, actual_2)


    def test_banner_url(self):
        manga = Manga.objects.create(
            name="Manga Image",
            romaji="Manga Image",
            description="Manga Image manga",
            status="RELEASING",
            start_date=datetime.now(),
            banner_url="https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx108556-NHjkz0BNJhLx.jpg"
        )
        expected_1 = "/media/heroes/manga-image/hero.jpeg"
        actual_1 = utility.banner_url(manga)
        self.assertEquals(expected_1, actual_1)
        expected_2 = ""
        actual_2 = utility.banner_url(self.no_image)
        self.assertEquals(expected_2, actual_2)


    def test_collected(self):
        user = User(
            username="BobbyBadBoi", email="bobby@badboi.com"
        )
        volume = Volume()
        expected = False
        actual = utility.collected(volume, user)
        self.assertEquals(expected, actual)


    def test_get_field_value(self):
        test_instance = UtilityTesterClass("I am attr1", None)
        expected_1 = "I am attr1"
        actual_1 = utility.get_field_value(test_instance, "attr1")
        self.assertEquals(expected_1, actual_1)
        expected_2 = "Unknown"
        actual_2 = utility.get_field_value(test_instance, "dummy_field")
        self.assertEquals(expected_2, actual_2)
        expected_3 = "Unknown"
        actual_3 = utility.get_field_value(test_instance, "attr2")
        self.assertEquals(expected_3, actual_3)


    def test_listify(self):
        value = "<script>console.log('HELLO THERE')</script>\nChapter 1\n \n\nChapter 2\n\n|I'm an arc\nChapter 3"
        expected = "<p class=\"\">scriptconsole.log('HELLO THERE')/script</p>\n<p class=\"\">Chapter 1</p>\n<p class=\"\">Chapter 2</p>\n<p class=\"font-bold my-2 text-lg underline\">I'M An Arc arc starts here</p>\n<p class=\"\">Chapter 3</p>"
        actual = utility.listify(value)
        self.assertEquals(expected, actual)
