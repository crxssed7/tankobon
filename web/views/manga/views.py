from django.shortcuts import render, get_object_or_404, redirect
from api.models import Manga, Volume
from web.forms import MangaForm
from django.contrib.auth.decorators import login_required
from tankobon.utils import mongo_log
import textwrap
import base64
import requests


def detail(request, manga_id):
    manga = get_object_or_404(Manga, id=manga_id)

    open_vol_request = request.GET.get('volume')
    open_vol = -1
    try:
        open_vol = int(open_vol_request)
    except BaseException:
        # If the volume the user provided is not a number, just default to the non tankobon chapters
        open_vol = -1

    volumes = Volume.objects.filter(manga=manga, absolute_number__gte=0).order_by('absolute_number')
    nontankobon = Volume.objects.filter(manga=manga, absolute_number__lt=0).first()

    return render(request, 'web/detail.html', context={'manga': manga, 'data': volumes,
                  'chapters_nonvolumed': nontankobon, 'search_active': 'active', 'open_vol': open_vol})


def widget(request, manga_id):
    manga = get_object_or_404(Manga, id=manga_id)
    title = manga.name
    n = 25
    start = 9.6585464
    # Wraps text so that it looks good in SVG
    wrapper = textwrap.TextWrapper(width=n)
    titles = wrapper.wrap(text=title)
    dic = []
    for i in range(len(titles)):
        t = {}
        t['value'] = titles[i]
        t['step'] = start
        dic.append(t)
        start += 7

    # Get base64 of image
    poster = ''
    if manga.poster:
        poster = 'data:image/png;base64,' + base64.b64encode(requests.get(manga.poster).content).decode('utf-8')
    return render(request, 'web/widget.svg', context={'manga': manga, 'titles': dic[:5], 'poster': poster}, content_type="image/svg+xml")


@login_required
def new_manga(request):
    if request.method == 'POST':
        form = MangaForm(request.POST)
        if form.is_valid():
            manga = form.save(commit=False)
            manga.locked = False
            manga.save()
            mongo_log('New Manga', manga.name, request.POST, request.user.username)
            return redirect('manga', manga_id=manga.id)
    else:
        form = MangaForm()
    return render(request, 'web/create.html', {'form': form, 'message': 'Add a manga', 'previous': '/manga/', 'type': 'manga'})


@login_required
def edit_manga(request, manga_id):
    manga_obj = get_object_or_404(Manga, id=manga_id)

    if manga_obj.locked == False:
        if request.method == 'POST':
            form = MangaForm(request.POST, instance=manga_obj)
            if form.is_valid():
                manga = form.save()
                mongo_log('Edit Manga', manga_obj.name, request.POST, request.user.username)
                return redirect('manga', manga_id=manga.id)
        else:
            form = MangaForm(instance=manga_obj)
        return render(request, 'web/manga_edit.html', {'form': form, 'manga': manga_obj})
    else:
        # Manga cannot be edited
        return render(request, 'web/manga_edit.html', {'locked': True})


def all_manga(request):
    manga = Manga.objects.all().order_by('name')[:8]
    manga_count = Manga.objects.count()
    return render(request, 'web/all.html', {'results': manga, 'count': manga_count, 'search_active': 'active', 'type': 'all'})


def all_manga_completed(request):
    manga = Manga.objects.filter(status="FINISHED").order_by('name')[:8]
    manga_count = Manga.objects.filter(status="FINISHED").count()
    return render(request, 'web/all.html', {'results': manga, 'count': manga_count, 'search_active': 'active', 'type': 'completed'})


def all_manga_releasing(request):
    manga = Manga.objects.filter(status="RELEASING").order_by('name')[:8]
    manga_count = Manga.objects.filter(status="RELEASING").count()
    return render(request, 'web/all.html', {'results': manga, 'count': manga_count, 'search_active': 'active', 'type': 'releasing'})
