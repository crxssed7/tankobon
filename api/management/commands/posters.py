import time

from django.core.management.base import BaseCommand

from api.models import Manga, Volume


class Command(BaseCommand):
    help = "Regenerates posters for all manga"

    def add_arguments(self, parser):
        parser.add_argument(
            "--volume",
            help="Regenerate posters for volumes that belong to a specific manga",
        )

    def handle(self, *args, **options):
        queryset = None
        if options["volume"]:
            queryset = Volume.objects.filter(manga=options["volume"]).exclude(
                poster_url="", absolute_number=-1
            )
        else:
            queryset = Manga.objects.exclude(poster_url="")

        for obj in queryset:
            print(obj)
            obj.get_remote_poster()
            obj.save()
            time.sleep(2)
