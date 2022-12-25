import json

from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse, HttpResponse

from .models import Manga, Volume

# Create your views here.


def get_manga(request):
    offset = request.GET.get("offset")
    _limit = request.GET.get("limit")
    query = request.GET.get("q")
    sort = request.GET.get("sort")
    status = request.GET.get("status")
    sort_field = "name"
    try:
        offset = int(offset)
    except BaseException:
        offset = 0
    if sort:
        if sort.lower() == "last_updated":
            sort_field = "-last_updated"
    limit = 8
    if _limit:
        try:
            limit = int(_limit)
        except BaseException:
            limit = 8
    manga = []
    total_results = 0
    if not query:
        results = []
        if status:
            results = list(
                Manga.objects.filter(status=status.upper())
                .values()
                .order_by(sort_field)
            )
        else:
            results = list(Manga.objects.values().order_by(sort_field))
        total_results = len(results)
        manga = results[offset : offset + limit]
    else:
        results = []
        if status:
            results = list(
                Manga.objects.filter(
                    Q(name__icontains=query) | Q(romaji__icontains=query),
                    status=status.upper(),
                )
                .values()
                .order_by(sort_field)
            )
        else:
            results = list(
                Manga.objects.filter(
                    Q(name__icontains=query) | Q(romaji__icontains=query)
                )
                .values()
                .order_by(sort_field)
            )
        total_results = len(results)
        manga = results[offset : offset + limit]
    total = Manga.objects.count()
    data = {"total": total, "total_results": total_results, "manga": manga}
    return JsonResponse(data=data)


def get_specific_manga(request, manga_id):
    try:
        manga = Manga.objects.get(id=manga_id)
        data = serializers.serialize(
            "json",
            [
                manga,
            ],
        )
        struct = json.loads(data)
        struct = struct[0]["fields"]
        struct.update({"id": manga_id})
        data = json.dumps(struct)
        return HttpResponse(data, content_type="application/json")
    except BaseException:
        return HttpResponse(
            json.dumps({"error": "Manga does not exist"}),
            content_type="application/json",
            status=404,
        )


def get_manga_volumes(request, manga_id):
    try:
        manga = Manga.objects.get(id=manga_id)
        # Get the volumes
        volumes = Volume.objects.filter(manga=manga, absolute_number__gte=0).order_by(
            "absolute_number"
        )
        volume_nt = Volume.objects.filter(manga=manga, absolute_number=-1).first()
        vols_data = []
        for volume in volumes:
            data = {"number": volume.absolute_number, "poster": volume.poster_url}
            chapters = []
            chapters_str = volume.chapters.strip().splitlines()
            for c in chapters_str:
                if not c.isspace():
                    chapters.append(c)
            data.update({"chapters": chapters})
            vols_data.append(data)

        if volume_nt:
            # Add the no tankobon chapters
            data = {"number": volume_nt.absolute_number, "poster": ""}
            chapters = []
            chapters_str = volume_nt.chapters.strip().splitlines()
            for c in chapters_str:
                if not c.isspace():
                    chapters.append(c)
            data.update({"chapters": chapters})
            vols_data.append(data)

        data = json.dumps(vols_data)
        return HttpResponse(data, content_type="application/json")
    except BaseException:
        return HttpResponse(
            json.dumps({"error": "Manga does not exist"}),
            content_type="application/json",
            status=404,
        )
