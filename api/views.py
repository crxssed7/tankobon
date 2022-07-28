from django.shortcuts import render
from django.http import JsonResponse
from .models import Manga
from django.db.models import Q

# Create your views here.
def get_manga(request):
    offset = request.GET.get('offset')
    query = request.GET.get('q')
    try:
        offset = int(offset)
    except:
        offset = 0
    limit = 8
    manga = []
    if not query:
        manga = list(Manga.objects.values().order_by('name')[offset:offset + limit])
    else:
        manga = list(Manga.objects.filter(Q(name__icontains=query) | Q(romaji__icontains=query)).values().order_by('name')[offset:offset + limit])
    data = {
        'manga': manga
    }
    return JsonResponse(data=data)