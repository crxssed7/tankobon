from django.shortcuts import render, get_object_or_404, redirect
from api.models import Manga, Volume
from django.views.generic import TemplateView, ListView, CreateView
from django.db.models import Q, Count
from .forms import MangaForm, VolumeEditForm, VolumeNewForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from tankobon.utils import mongo_log
import textwrap
import base64
import requests

# Create your views here.
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def index(request):
    manga = Manga.objects.all().order_by('-last_updated')[:4]
    return render(request, 'web/index.html', context={'home_active': 'active', 'results': manga})

def contrib(request):
    return render(request, 'web/contrib.html')

def docs(request):
    return render(request, 'web/api.html')

def changelog(request):
    return render(request, 'web/changelog.html')

def helpneeded(request):
    no_volume = Manga.objects.exclude(status="PLANNED").annotate(cnt=Count('volume')).filter(cnt=0)
    no_poster = Manga.objects.filter(poster='')
    ctx = {
        'no_volume': no_volume,
        'no_poster': no_poster
    }
    return render(request, 'web/help.html', context=ctx)

class SearchResultsView(ListView):
    model = Manga
    template_name = 'web/search.html'

    def get_queryset(self): 
        query = self.request.GET.get("q")
        if query:
            object_list = Manga.objects.filter(Q(name__icontains=query) | Q(romaji__icontains=query))
        else:
            object_list = []
        return object_list

    def get_context_data(self,**kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['recently_updated'] = Manga.objects.all().order_by('-last_updated')[:8]
        context['releasing'] = Manga.objects.filter(status="RELEASING").order_by('-last_updated')[:5]
        context['completed'] = Manga.objects.filter(status="FINISHED").order_by('-last_updated')[:5]
        context['search_active'] = 'active'
        q = self.request.GET.get("q")
        if q:
            context['query'] = q
        return context

def detail(request, manga_id):
    manga = get_object_or_404(Manga, id=manga_id)

    open_vol_request = request.GET.get('volume')
    open_vol = -1
    try:
        open_vol = int(open_vol_request)
    except:
        # If the volume the user provided is not a number, just default to the non tankobon chapters
        open_vol = -1

    volumes = Volume.objects.filter(manga=manga, absolute_number__gte=0).order_by('absolute_number')
    nontankobon = Volume.objects.filter(manga=manga, absolute_number__lt=0).first()

    return render(request, 'web/detail.html', context={'manga': manga, 'data': volumes, 'chapters_nonvolumed': nontankobon, 'search_active': 'active', 'open_vol': open_vol})

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
    return render(request, 'web/widget.html', context={'manga': manga, 'titles': dic[:5], 'poster': poster}, content_type="image/svg+xml")

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

@login_required
def edit_volume(request, manga_id, volume_number):
    volume = Volume.objects.filter(manga=manga_id, absolute_number=volume_number).first()
    if volume:
        if volume.locked == False:
            if request.method == 'POST':
                form = VolumeEditForm(request.POST, instance=volume)
                if form.is_valid():
                    v = form.save(commit=False)
                    v.absolute_number = volume.absolute_number
                    v.manga = volume.manga
                    v.save()
                    mongo_log('Edit Volume', volume.manga.name, str(v) + '\n' + v.chapters, request.user.username)
                    return redirect('manga', manga_id=v.manga.id)
            else:
                form = VolumeEditForm(instance=volume)
            return render(request, 'web/volume_edit.html', {'form': form, 'volume': volume})
        else:
            return render(request, 'web/volume_edit.html', {'locked': True})
    else:
        raise Http404("Page not found")

@login_required
def edit_non_volume(request, manga_id):
    volume = Volume.objects.filter(manga=manga_id, absolute_number__lt=0).first()
    if volume:
        if volume.locked == False:
            if request.method == 'POST':
                form = VolumeEditForm(request.POST, instance=volume)
                if form.is_valid():
                    v = form.save(commit=False)
                    v.absolute_number = volume.absolute_number
                    v.manga = volume.manga
                    v.save()
                    mongo_log('Edit Volume', volume.manga.name, str(v) + '\n' + v.chapters, request.user.username)
                    return redirect('manga', manga_id=v.manga.id)
            else:
                form = VolumeEditForm(instance=volume)
            return render(request, 'web/volume_edit.html', {'form': form, 'volume': volume})
        else:
            return render(request, 'web/volume_edit.html', {'locked': True})
    else:
        raise Http404("Page not found")

@login_required
def new_volume(request, manga_id):
    manga = get_object_or_404(Manga, id=manga_id)
    if not manga.locked:
        if request.method == 'POST':
            data = request.POST.copy()
            data['manga'] = manga.id
            form = VolumeNewForm(data)
            if form.is_valid():
                v = form.save(commit=False)
                v.manga = manga
                v.locked = False
                v.save()
                mongo_log('New Volume', manga.name, str(v) + '\n' + v.chapters, request.user.username)
                return redirect('manga', manga_id=manga.id)
        else:
            form = VolumeNewForm()
        return render(request, 'web/create.html', {'form': form, 'message': 'Add a volume', 'subnote': manga.name, 'previous': '/manga/' + str(manga.id) + '/', 'type': 'volume'})
    else:
        raise Http404("Page not found")

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