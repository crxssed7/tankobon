from django.db import models

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
    anilist_id = models.PositiveIntegerField(blank=True)
    mal_id = models.PositiveIntegerField(blank=True)
    mangaupdates_id = models.PositiveIntegerField(blank=True)
    anime_planet_slug = models.CharField(max_length=100, blank=True)
    kitsu_id = models.PositiveIntegerField(blank=True)
    magazine = models.CharField(max_length=150, blank=True, null=True)
    volume_count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

class Chapter(models.Model):
    class Meta:
        unique_together = (('volume', 'chapter_number', 'manga'),)
    
    name = models.CharField(max_length=100, blank=True, null=True)
    volume = models.IntegerField(default=-1)
    chapter_number = models.FloatField()
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)

    def __str__(self):
        return self.manga.name + ' Chp.' + str(self.chapter_number)