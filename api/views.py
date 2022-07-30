from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
from .models import Manga, Volume
from django.db.models import Q
import json

# Create your views here.
def get_manga(request):
    offset = request.GET.get('offset')
    _limit = request.GET.get('limit')
    query = request.GET.get('q')
    sort = request.GET.get('sort')
    sort_field = 'name'
    try:
        offset = int(offset)
    except:
        offset = 0
    if sort:
        if sort.lower() == 'last_updated':
            sort_field = '-last_updated'
    limit = 8
    if _limit:
        try:
            limit = int(_limit)
        except:
            limit = 8
    manga = []
    if not query:
        manga = list(Manga.objects.values().order_by(sort_field)[offset:offset + limit])
    else:
        manga = list(Manga.objects.filter(Q(name__icontains=query) | Q(romaji__icontains=query)).values().order_by(sort_field)[offset:offset + limit])
    data = {
        'manga': manga
    }
    return JsonResponse(data=data)

def get_specific_manga(request, manga_id):
    try:
        manga = Manga.objects.get(id=manga_id)
        data = serializers.serialize('json', [manga,])
        struct = json.loads(data)
        struct = struct[0]['fields']
        struct.update({'id': manga_id})
        data = json.dumps(struct)
        return HttpResponse(data, content_type='application/json')
    except:
        return HttpResponse(json.dumps({'error': 'Manga does not exist'}), content_type='application/json', status=404)

def get_manga_volumes(request, manga_id):
    try:
        manga = Manga.objects.get(id=manga_id)
        # Get the volumes
        volumes = Volume.objects.filter(manga=manga).order_by('absolute_number')
        vols_data = []
        for volume in volumes:
            data = {
                "number": volume.absolute_number,
                "poster": volume.poster
            }
            chapters = []
            chapters_str = volume.chapters.strip().splitlines()
            for c in chapters_str:
                if not c.isspace():
                    chapters.append(c)
            data.update({"chapters": chapters})
            vols_data.append(data)
        data = json.dumps(vols_data)
        return HttpResponse(data, content_type='application/json')
    except:
        return HttpResponse(json.dumps({'error': 'Manga does not exist'}), content_type='application/json', status=404)