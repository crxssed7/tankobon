from django.test import SimpleTestCase, TestCase
from django.utils.timezone import datetime

from api.models import Volume, Manga, Edition
from web.forms import MangaForm, SignUpForm, EditionForm, VolumeForm


class TestMangaForms(SimpleTestCase):
    def test_manga_form_with_valid_data(self):
        form = MangaForm(
            data={
                "name": "Two Piece",
                "romaji": "Two Piece",
                "description": "haha funi",
                "status": "RELEASING",
                "start_date": "2012-05-15",
                "poster_url": "",
                "banner_url": "",
                "anilist_id": "",
                "mal_id": "",
                "mangaupdates_id": "",
                "anime_planet_slug": "",
                "kitsu_id": "",
                "fandom": "",
                "magazine": "",
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
                "start_date": "This should be a date",
                "poster_url": "",
                "banner_url": "",
                "anilist_id": "",
                "mal_id": "",
                "mangaupdates_id": "",
                "anime_planet_slug": "",
                "kitsu_id": "",
                "fandom": "",
                "magazine": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)


class TestEditionForm(TestCase):
    def test_edition_form_with_valid_data(self):
        manga = Manga.objects.create(
            name="Fullmetal Alchemist",
            romaji="Fullmetal Alchemist",
            description="Fullmetal Alchemist manga",
            status="FINISHED",
            start_date=datetime.now(),
        )
        form = EditionForm(data={"manga": manga, "name": "fullmetal"})

        self.assertTrue(form.is_valid())

    def test_edition_form_with_invalid_data(self):
        form = EditionForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)


class TestVolumeForms(TestCase):
    def test_volume_form_does_not_update_absolute_number(self):
        manga = Manga.objects.create(
            name="Assassination Classroom",
            romaji="Assassination Classroom",
            description="Assassination Classroom manga",
            status="RELEASING",
            start_date=datetime.now(),
        )
        volume = Volume.objects.create(absolute_number=1, manga=manga)
        form = VolumeForm(
            manga=manga,
            data={
                "absolute_number": 2,
                "poster_url": "",
                "chapters": "Chapter 1\nChapter 2",
                "release_date": "2012-05-15",
                "page_count": 300,
                "isbn": "9784091241023"
            },
            instance=volume,
        )
        v = form.save()

        self.assertEquals(v.absolute_number, 1)
        self.assertEquals(v.chapters, "Chapter 1\nChapter 2")

    def test_volume_form_does_not_accept_certain_fields_for_non_tankobon(self):
        manga = Manga.objects.create(
            name="Assassination Classroom",
            romaji="Assassination Classroom",
            description="Assassination Classroom manga",
            status="RELEASING",
            start_date=datetime.now(),
        )
        volume = Volume.objects.create(absolute_number=-1, manga=manga)
        form = VolumeForm(
            manga=manga,
            data={
                "absolute_number": 2,
                "poster_url": "https://tankobon.s3.amazonaws.com/posters/mob-psycho-100/volumes/standard-japanese/volume_1_poster.png",
                "chapters": "Chapter 1\nChapter 2",
                "release_date": "2012-05-15",
                "isbn": "9784091241023",
                "page_count": 200
            },
            instance=volume,
        )
        self.assertEquals(form.is_valid(), True)
        self.assertEquals(form.cleaned_data, {"chapters": "Chapter 1\nChapter 2"})
        v = form.save()
        self.assertEquals(v.poster_url, "")
        self.assertEquals(v.release_date, None)
        self.assertEquals(v.isbn, None)
        self.assertEquals(v.page_count, None)
        self.assertEquals(v.chapters, "Chapter 1\nChapter 2")

    def test_volume_form_with_valid_data(self):
        manga = Manga.objects.create(
            name="Demon Slayer",
            romaji="Demon Slayer",
            description="Demon Slayer manga",
            status="RELEASING",
            start_date=datetime.now(),
        )
        form = VolumeForm(
            manga=manga,
            data={
                "absolute_number": 1,
                "poster_url": "",
                "chapters": "Chapter 1\nChapter 2",
                "manga": manga,
                "edition": Edition.objects.first(),
                "release_date": "2012-05-15",
                "page_count": 300,
                "isbn": "9784091241023"
            },
        )
        self.assertTrue(form.is_valid())

    def test_volume_form_with_invalid_data(self):
        manga = Manga.objects.create(
            name="Demon Slayer",
            romaji="Demon Slayer",
            description="Demon Slayer manga",
            status="RELEASING",
            start_date=datetime.now(),
        )
        form = VolumeForm(manga=manga, data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)
        self.assertIn('absolute_number', form.errors.keys())
        self.assertIn('This field is required.', form.errors['absolute_number'])
        self.assertIn('edition', form.errors.keys())
        self.assertIn('This field is required.', form.errors['edition'])
        self.assertIn('chapters', form.errors.keys())
        self.assertIn('This field is required.', form.errors['chapters'])

    def test_volume_form_when_absolute_number_exists(self):
        manga = Manga.objects.create(
            name="Chainsaw Man",
            romaji="Chainsaw Man",
            description="Chainsaw Man manga",
            status="RELEASING",
            start_date=datetime.now(),
        )
        edition = Edition.objects.first()
        volume = Volume.objects.create(absolute_number=1, manga=manga, edition=edition)
        form = VolumeForm(
            manga=manga,
            data={
                "absolute_number": 1,
                "poster_url": "",
                "chapters": "Chapter 1\nChapter 2",
                "manga": manga,
                "edition": edition,
                "release_date": "2012-05-15",
                "page_count": 300,
                "isbn": "9784091241023"
            },
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertIn('absolute_number', form.errors.keys())
        self.assertIn('Volume with this absolute_number already exists for this manga edition', form.errors['absolute_number'])


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
