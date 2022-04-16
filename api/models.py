from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True

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
    poster = models.URLField(blank=True, max_length=750)
    banner = models.URLField(blank=True, max_length=750)
    anilist_id = models.PositiveIntegerField(blank=True, null=True)
    mal_id = models.PositiveIntegerField(blank=True, null=True)
    mangaupdates_id = models.PositiveIntegerField(blank=True, null=True)
    anime_planet_slug = models.CharField(max_length=100, blank=True, null=True)
    kitsu_id = models.PositiveIntegerField(blank=True, null=True)
    fandom = models.URLField(blank=True, null=True)
    magazine = models.CharField(max_length=150, blank=True, null=True)
    volume_count = models.PositiveIntegerField(default=1)
    locked = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Volume(models.Model):
    class Meta:
        unique_together = ('absolute_number', 'manga')

    absolute_number = models.IntegerField(default=-1)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    chapters = models.TextField()
    locked = models.BooleanField(default=False)

    def __str__(self):
        if self.absolute_number >= 0:
            return self.manga.name + ' Volume ' + str(self.absolute_number)
        else:
            return self.manga.name + ' Non-tankobon'