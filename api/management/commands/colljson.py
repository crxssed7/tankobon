from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from api.models import Manga, Collection


class Command(BaseCommand):
    help = "Regenerates posters for all manga"

    def add_arguments(self, parser):
        parser.add_argument(
            "--manga",
            help="Get all the collections for the manga",
        )

    def handle(self, *args, **options):
        user = User.objects.first()
        manga = Manga.objects.get(id=options["manga"])
        print(manga.name)
        collections = Collection.objects.filter(user=user, volume__manga=manga)
        data = []
        for coll in collections:
            data.append({"volume": coll.volume.absolute_number, "date": coll.collected_at.strftime("%Y-%m-%d")})
        print(data)
