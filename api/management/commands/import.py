import requests

from django.core.management.base import BaseCommand
from django.db import Error
from django.utils.timezone import datetime

from api.models import Manga


class Command(BaseCommand):
    help = "Imports Manga from AniList"

    def _graphql(self, manga_id):
        return """
query ($id: Int) {
  Media(id: $id, type: MANGA) {
    title {
      romaji
      english
      native
      userPreferred
    },
    description,
    status,
    startDate {
      year
      month
      day
    },
    coverImage {
      extraLarge
      large
      medium
      color
    },
    bannerImage,
    id,
    idMal,
    volumes
  }
}
"""

    def add_arguments(self, parser):
        parser.add_argument("manga_id", type=int)

    def handle(self, *args, **options):
        manga_id = options["manga_id"]

        # We need to send a request to AniList API
        query = self._graphql(manga_id=manga_id)
        variables = {"id": manga_id}
        response = requests.post(
            "https://graphql.anilist.co", json={"query": query, "variables": variables}
        )
        if response.status_code == 200:
            json = response.json()

            volume_count = json["data"]["Media"]["volumes"]
            if not volume_count:
                volume_count = int(
                    input(
                        "There was no volume count found in the API. Specify the volume count: "
                    )
                )

            if (
                json["data"]["Media"]["startDate"]["month"]
                and json["data"]["Media"]["startDate"]["day"]
            ):
                start_date = datetime(
                    year=json["data"]["Media"]["startDate"]["year"],
                    month=json["data"]["Media"]["startDate"]["month"],
                    day=json["data"]["Media"]["startDate"]["day"],
                )
            else:
                start_date = input(
                    "There was no start date found in the API. Specify the start date (YYYY-MM-DD): "
                )

            name = json["data"]["Media"]["title"]["english"]
            if not name:
                name = input(
                    "There was no English name found in the API. Specify the English name: "
                )

            romaji = json["data"]["Media"]["title"]["romaji"]
            if not romaji:
                romaji = name

            status = str(json["data"]["Media"]["status"])

            banner = json["data"]["Media"]["bannerImage"]
            if not banner:
                banner = ""

            try:
                Manga.objects.create(
                    name=name,
                    romaji=romaji,
                    description=json["data"]["Media"]["description"],
                    status=status.upper(),
                    start_date=start_date,
                    poster_url=json["data"]["Media"]["coverImage"]["large"],
                    banner_url=banner,
                    anilist_id=manga_id,
                    mal_id=json["data"]["Media"]["idMal"],
                    volume_count=volume_count,
                )
            except Error as exception:
                print("There was an error:")
                print(exception)
        else:
            print("Error: There was no manga found with that ID")
