from django.shortcuts import render
from django.http import JsonResponse
from .models import Manga
from django.db.models import Q

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