from django.test import SimpleTestCase, TestCase
from django.utils.timezone import datetime

from api.models import Volume, Manga
from web.forms import MangaForm, VolumeEditForm, VolumeNewForm, SignUpForm


class TestMangaForms(SimpleTestCase):
    def test_manga_form_with_valid_data(self):
        form = MangaForm(
            data={
                "name": "Two Piece",
                "romaji": "Two Piece",
                "description": "haha funi",
                "status": "RELEASING",
                "start_date": "2012-05-15",
                "poster": "",
                "banner": "",
                "anilist_id": "",
                "mal_id": "",
                "mangaupdates_id": "",
                "anime_planet_slug": "",
                "kitsu_id": "",
                "fandom": "",
                "magazine": "",
                "volume_count": 23,
            }
        )

        self.assertTrue(form.is_valid())

    def test_manga_form_with_invalid_data(self):
        form = MangaForm(
            data={
                "name": "Two Piece",
                "romaji": "Two Piece",
                "description": "haha funi",
                "status": "RELEASING",
                "start_date": "2012-05-15",
                "poster": "",
                "banner": "",
                "anilist_id": "",
                "mal_id": "",
                "mangaupdates_id": "",
                "anime_planet_slug": "",
                "kitsu_id": "",
                "fandom": "",
                "magazine": "",
                "volume_count": "this should be a number",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class TestVolumeForms(TestCase):
    def test_volume_edit_form_with_valid_data(self):
        form = VolumeEditForm(data={"poster": "", "chapters": "Chapter 1\nChapter 2"})

        self.assertTrue(form.is_valid())

    def test_volume_edit_form_with_invalid_data(self):
        form = VolumeEditForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_volume_edit_form_does_not_update_absolute_number(self):
        manga = Manga.objects.create(
            name="Assassination Classroom",
            romaji="Assassination Classroom",
            description="Assassination Classroom manga",
            status="RELEASING",
            start_date=datetime.now(),
        )
        volume = Volume.objects.create(absolute_number=1, manga=manga)
        form = VolumeEditForm(
            data={
                "absolute_number": 2,
                "poster": "",
                "chapters": "Chapter 1\nChapter 2",
            },
            instance=volume,
        )
        v = form.save()

        self.assertEquals(v.absolute_number, 1)
        self.assertEquals(v.chapters, "Chapter 1\nChapter 2")

    def test_volume_new_form_with_valid_data(self):
        manga = Manga.objects.create(
            name="Demon Slayer",
            romaji="Demon Slayer",
            description="Demon Slayer manga",
            status="RELEASING",
            start_date=datetime.now(),
        )
        form = VolumeNewForm(
            data={
                "absolute_number": 1,
                "poster": "",
                "chapters": "Chapter 1\nChapter 2",
                "manga": manga,
            }
        )

        self.assertTrue(form.is_valid())

    def test_volume_new_form_with_invalid_data(self):
        form = VolumeNewForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_volume_new_form_when_absolute_number_exists(self):
        manga = Manga.objects.create(
            name="Chainsaw Man",
            romaji="Chainsaw Man",
            description="Chainsaw Man manga",
            status="RELEASING",
            start_date=datetime.now(),
        )
        volume = Volume.objects.create(absolute_number=1, manga=manga)
        form = VolumeNewForm(
            data={
                "absolute_number": 1,
                "poster": "",
                "chapters": "Chapter 1\nChapter 2",
                "manga": manga,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class TestAccountForms(TestCase):
    def test_signup_form_with_valid_data(self):
        form = SignUpForm(
            data={
                "username": "HelloThere",
                "email": "obaewankenobi@itsatrap.com",
                "password1": "GENERALKENOBI!",
                "password2": "GENERALKENOBI!",
            }
        )

        self.assertTrue(form.is_valid())

    def test_signup_form_with_invalid_data(self):
        form = SignUpForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_signup_form_email_is_required(self):
        form = SignUpForm(
            data={
                "username": "HelloThere",
                "password1": "GENERALKENOBI!",
                "password2": "GENERALKENOBI!",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)