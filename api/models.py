import io
import requests

from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.timezone import datetime

from simple_history.models import HistoricalRecords

User._meta.get_field("email")._unique = True

# Create your models here.


class Manga(models.Model):
    STATUS_CHOICES = (
        ("RELEASING", "Releasing"),
        ("FINISHED", "Finished"),
        ("PLANNED", "Planned"),
    )

    name = models.CharField(max_length=100)
    romaji = models.CharField(max_length=150)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    start_date = models.DateField()
    poster_url = models.URLField(blank=True, max_length=750)
    poster_file = models.ImageField(upload_to="posters", blank=True, null=True)
    banner_url = models.URLField(blank=True, max_length=750)
    banner_file = models.ImageField(upload_to="banners", blank=True, null=True)
    anilist_id = models.PositiveIntegerField(blank=True, null=True)
    mal_id = models.PositiveIntegerField(blank=True, null=True)
    mangaupdates_id = models.PositiveIntegerField(blank=True, null=True)
    anime_planet_slug = models.CharField(max_length=100, blank=True, null=True)
    kitsu_id = models.PositiveIntegerField(blank=True, null=True)
    fandom = models.URLField(blank=True, null=True)
    magazine = models.CharField(max_length=150, blank=True, null=True)
    volume_count = models.PositiveIntegerField(default=1)
    locked = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(excluded_fields=["last_updated"])

    _original_poster = None
    _original_banner = None

    def __init__(self, *args, **kwargs):
        super(Manga, self).__init__(*args, **kwargs)
        self._original_poster = self.poster_url
        self._original_banner = self.banner_url

    def __str__(self):
        return str(self.name)

    def get_remote_banner(self):
        if self.banner_url:
            result = requests.get(self.banner_url)
            if result.status_code == 200:
                content_type = result.headers["Content-Type"]
                if content_type.startswith("image/"):
                    ext = content_type.split("/")[-1]
                    self.banner_file.delete(save=False)
                    image = ImageFile(
                        io.BytesIO(result.content),
                        name=f"{slugify(self.name)}/banner.{ext}",
                    )
                    self.banner_file = image
        else:
            if self.banner_file:
                self.banner_file.delete(save=False)

    def get_remote_poster(self):
        if self.poster_url:
            result = requests.get(self.poster_url)
            if result.status_code == 200:
                content_type = result.headers["Content-Type"]
                if content_type.startswith("image/"):
                    ext = content_type.split("/")[-1]
                    self.poster_file.delete(save=False)
                    image = ImageFile(
                        io.BytesIO(result.content),
                        name=f"{slugify(self.name)}/poster.{ext}",
                    )
                    self.poster_file = image
        else:
            if self.poster_file:
                self.poster_file.delete(save=False)

    def save(self, *args, **kwargs):
        primary = self.pk
        if self._original_poster != self.poster_url or primary == None:
            self.get_remote_poster()

        if self._original_banner != self.banner_url or primary == None:
            self.get_remote_banner()
        super(Manga, self).save(*args, **kwargs)


class Edition(models.Model):
    class Meta:
        unique_together = ("name", "manga")

    name = models.CharField(max_length=150)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.manga.name}: {self.name.capitalize()} Edition"

    def save(self, *args, **kwargs):
        self.name = self.name.lower().strip()
        if self.name.endswith("edition"):
            self.name = self.name.replace("edition", "").strip()
        super(Edition, self).save(*args, **kwargs)


class Volume(models.Model):
    class Meta:
        unique_together = ("absolute_number", "manga", "edition")
        ordering = ["absolute_number"]

    absolute_number = models.IntegerField(
        default=-1, validators=[MinValueValidator(-1)]
    )
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    chapters = models.TextField()
    locked = models.BooleanField(default=False)
    poster_url = models.URLField(blank=True, max_length=750)
    poster_file = models.ImageField(upload_to="posters", blank=True, null=True)
    edition = models.ForeignKey(
        Edition, blank=True, null=True, on_delete=models.CASCADE
    )
    history = HistoricalRecords()

    _original_poster = None

    def __init__(self, *args, **kwargs):
        super(Volume, self).__init__(*args, **kwargs)
        self._original_poster = self.poster_url

    def get_remote_poster(self):
        if self.poster_url:
            result = requests.get(self.poster_url)
            if result.status_code == 200:
                content_type = result.headers["Content-Type"]
                if content_type.startswith("image/"):
                    ext = content_type.split("/")[-1]
                    self.poster_file.delete(save=False)
                    image = ImageFile(
                        io.BytesIO(result.content),
                        name=f"{slugify(self.manga.name)}/volumes/{self.edition.name}_volume_{self.absolute_number}_poster.{ext}",
                    )
                    self.poster_file = image
        else:
            if self.poster_file:
                self.poster_file.delete(save=False)

    def save(self, *args, **kwargs):
        primary = self.pk
        if self._original_poster != self.poster_url or primary == None:
            self.get_remote_poster()
        super(Volume, self).save(*args, **kwargs)

    def __str__(self):
        if self.absolute_number >= 0:
            return self.manga.name + " Volume " + str(self.absolute_number)
        return self.manga.name + " Non-tankobon"


@receiver(post_save, sender=Volume)
# Update the mangas last updated field
def update_last_updated(sender, instance=None, created=False, **kwargs):
    now = datetime.now()
    manga = instance.manga
    manga.last_updated = now
    manga.save()


# When a new manga is created, we want to create a standard Edition for it
@receiver(post_save, sender=Manga)
def create_standard_edtion(sender, instance=None, created=False, **kwargs):
    if created:
        Edition.objects.create(name="standard", manga=instance)
