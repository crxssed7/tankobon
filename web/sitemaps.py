from django.contrib.auth.models import User
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from api.models import Manga

class SingleViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return [
            "index",
            "contrib",
            "help_needed",
            "search",
            "all_manga",
            "new_manga",
        ]

    def location(self, obj):
        return reverse(obj)


class MangaSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Manga.objects.all()

    def lastmod(self, obj):
        return obj.last_updated

    def location(self, obj):
        return reverse("manga", args=[obj.id])
