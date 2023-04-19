from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import slugify
from django.utils.timezone import datetime, now

from simple_history.models import HistoricalRecords
from simple_history import register as history_register

from api.decorators import track_data, track_data_performed
from api.tokens import account_activation_token
from api.mixins.models import RemoteImageFieldMixin
from api.validators import isbn_validator, image_url_validator

from tankobon.settings import DEFAULT_FROM_EMAIL

User._meta.get_field("email")._unique = True


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    icon = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Language(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=2, unique=True)

    @classmethod
    def japanese(cls):
        return Language.objects.filter(name="Japanese").first()

    def __str__(self):
        return str(self.name)


@track_data(
    "name",
    "romaji",
    "description",
    "status",
    "start_date",
    "poster_url",
    "poster_file",
    "banner_url",
    "banner_file",
    "anilist_id",
    "mal_id",
    "mangaupdates_id",
    "anime_planet_slug",
    "kitsu_id",
    "fandom",
    "magazine",
    "tags",
)
class Manga(RemoteImageFieldMixin, models.Model):
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
    poster_url = models.URLField(blank=True, max_length=750, validators=[image_url_validator])
    poster_file = models.ImageField(upload_to="posters", blank=True, null=True)
    banner_url = models.URLField(blank=True, max_length=750, validators=[image_url_validator])
    banner_file = models.ImageField(upload_to="heroes", blank=True, null=True)
    anilist_id = models.PositiveIntegerField(blank=True, null=True)
    mal_id = models.PositiveIntegerField(blank=True, null=True)
    mangaupdates_id = models.PositiveIntegerField(blank=True, null=True)
    anime_planet_slug = models.CharField(max_length=100, blank=True, null=True)
    kitsu_id = models.PositiveIntegerField(blank=True, null=True)
    fandom = models.URLField(blank=True, null=True)
    magazine = models.CharField(max_length=150, blank=True, null=True)
    locked = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    tags = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    is_oneshot = models.BooleanField(default=False)

    _original_poster = None
    _original_banner = None

    def __init__(self, *args, **kwargs):
        super(Manga, self).__init__(*args, **kwargs)
        self._original_poster = self.poster_url
        self._original_banner = self.banner_url

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        primary = self.pk
        if self._original_poster != self.poster_url or primary == None:
            self.get_remote_poster()

        if self._original_banner != self.banner_url or primary == None:
            self.get_remote_banner()
        super(Manga, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.poster_file:
            self.poster_file.delete(save=False)
        if self.banner_file:
            self.banner_file.delete(save=False)
        super(Manga, self).delete(*args, **kwargs)

    def poster_file_name(self, ext):
        return f"{slugify(self.name)}/poster.{ext}"

    def banner_file_name(self, ext):
        return f"{slugify(self.name)}/hero.{ext}"


history_register(Manga, inherit=True, excluded_fields=["last_updated"])


class Edition(models.Model):
    class Meta:
        unique_together = ("name", "manga")

    name = models.CharField(max_length=150)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.manga.name}: {self.name.title()} Edition"

    def save(self, *args, **kwargs):
        self.name = self.name.lower().strip()
        if self.name.endswith("edition"):
            self.name = self.name.replace("edition", "").strip()
        super(Edition, self).save(*args, **kwargs)


class Volume(RemoteImageFieldMixin, models.Model):
    class Meta:
        unique_together = ("absolute_number", "manga", "edition")
        ordering = ["absolute_number"]

    absolute_number = models.IntegerField(
        default=-1, validators=[MinValueValidator(-1)]
    )
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    chapters = models.TextField()
    locked = models.BooleanField(default=False)
    poster_url = models.URLField(blank=True, max_length=750, validators=[image_url_validator])
    poster_file = models.ImageField(upload_to="posters", blank=True, null=True)
    edition = models.ForeignKey(
        Edition, blank=True, null=True, on_delete=models.CASCADE
    )
    isbn = models.CharField(max_length=20, validators=[isbn_validator], blank=True, null=True, unique=True)
    page_count = models.PositiveIntegerField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    history = HistoricalRecords()

    _original_poster = None

    def __init__(self, *args, **kwargs):
        super(Volume, self).__init__(*args, **kwargs)
        self._original_poster = self.poster_url

    def save(self, *args, **kwargs):
        self.clean()

        primary = self.pk
        if self._original_poster != self.poster_url or primary == None:
            self.get_remote_poster()
        if self.isbn:
            self.isbn = self.isbn.replace("-", "")
        super(Volume, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.poster_file:
            self.poster_file.delete(save=False)
        super(Volume, self).delete(*args, **kwargs)

    def clean(self):
        super().clean()
        self.validate_oneshot()

    def __str__(self):
        if self.absolute_number >= 0:
            return self.manga.name + " Volume " + str(self.absolute_number)
        return self.manga.name + " Non-tankobon"

    def validate_oneshot(self):
        # Check if the manga is a oneshot and the edition does not already have a volume
        if self.manga.is_oneshot and self.edition.volume_set.exists():
            raise ValidationError("A oneshot manga can only have one volume.")

    def has_collected(self, user):
        return Collection.objects.filter(volume=self, user=user).exists()

    def poster_file_name(self, ext):
        return f"{slugify(self.manga.name)}/volumes/{slugify(self.edition.name)}/volume_{self.absolute_number}_poster.{ext}"

    # This isn't used. Maybe in the future we will have volume banners so I'll keep here for now.
    def banner_file_name(self, ext):
        return f"{slugify(self.manga.name)}/volumes/{slugify(self.edition.name)}/volume_{self.absolute_number}_banner.{ext}"


class Collection(models.Model):
    class Meta:
        unique_together = ("user", "edition", "volume")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
    volume = models.ForeignKey(Volume, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    collected_at = models.DateField(default=now)

    def save(self, *args, **kwargs):
        self.edition = self.volume.edition
        super(Collection, self).save(*args, **kwargs)


@receiver(pre_save, sender=Genre)
def update_genre_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


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
        japanese = Language.japanese()
        Edition.objects.create(name="standard japanese", manga=instance, language=japanese)


@receiver(track_data_performed, sender=Manga)
def manga_save_history(sender, instance, **kwargs):
    if not instance.whats_changed():
        instance.skip_history_when_saving = True

@receiver(post_save, sender=User)
def create_user_deps(sender, instance=None, created=False, **kwargs):
    if created:
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        token = account_activation_token.make_token(instance)

        html = loader.render_to_string("emails/signup.html", {
            "username": instance.username,
            "domain": Site.objects.all().first().domain,
            "uid": uid,
            "token": token
        })
        send_mail(
            "Activate your new Tankōbon account.",
            "Welcome to Tankōbon!",
            DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
            html_message=html
        )
