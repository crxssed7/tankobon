import time

from django.core.management.base import BaseCommand
from django.db import Error

from api.models import Manga


class Command(BaseCommand):
    help = "Regenerates banners for all manga"

    def handle(self, *args, **options):
        queryset = Manga.objects.exclude(banner_url="")

        for obj in queryset:
            print(obj)
            obj.get_remote_banner()
            obj.save()
            time.sleep(10)
