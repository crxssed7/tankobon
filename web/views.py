from django.shortcuts import render, get_object_or_404, redirect
from api.models import Manga, Volume
from django.views.generic import TemplateView, ListView, CreateView
from django.db.models import Q, Count
from .forms import MangaForm, VolumeEditForm, VolumeNewForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from tankobon.utils import matrix_notif

# Create your views here.
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def index(request):
    manga = Manga.objects.all().order_by('-id')[:4]
    return render(request, 'web/index.html', context={'home_active': 'active', 'results': manga})

def contrib(request):
    return render(request, 'web/contrib.html')

class SearchResultsView(ListView):
    model = Manga
    template_name = 'web/search.html'

    def get_queryset(self): # new
        query = self.request.GET.get("q")
        if query:
            object_list = Manga.objects.filter(Q(name__icontains=query) | Q(romaji__icontains=query))
        else:
            object_list = Manga.objects.all().order_by('-id')[:16]
        return object_list

    def get_context_data(self,**kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['search_active'] = 'active'
        q = self.request.GET.get("q")
        if q:
            context['query'] = q
        else:
            context['latest_msg'] = True
        return context

def detail(request, manga_id):
    manga = get_object_or_404(Manga, id=manga_id)

    volumes = Volume.objects.filter(manga=manga, absolute_number__gte=0).order_by('absolute_number')
    nontankobon = Volume.objects.filter(manga=manga, absolute_number__lt=0).first()

    return render(request, 'web/detail.html', context={'manga': manga, 'data': volumes, 'chapters_nonvolumed': nontankobon})

@login_required
def new_manga(request):
    if request.method == 'POST':
        form = MangaForm(request.POST)
        if form.is_valid():
            manga = form.save(commit=False)
            manga.locked = False
            manga.save()
            matrix_notif('new manga', manga, request.POST, request.user)
            return redirect('manga', manga_id=manga.id)
    else:
        form = MangaForm()
    return render(request, 'web/create.html', {'form': form, 'message': 'Add a manga', 'previous': '/manga/'})

@login_required
def edit_manga(request, manga_id):
    manga_obj = get_object_or_404(Manga, id=manga_id)

    if manga_obj.locked == False:
        if request.method == 'POST':
            form = MangaForm(request.POST, instance=manga_obj)
            if form.is_valid():
                manga = form.save()
                matrix_notif('edit manga', manga_obj, request.POST, request.user)
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
                    matrix_notif('edit volume', volume.manga, str(v) + '\n' + v.chapters, request.user)
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
                    matrix_notif('edit volume', volume.manga, str(v) + '\n' + v.chapters, request.user)
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
                matrix_notif('new volume', manga, str(v) + '\n' + v.chapters, request.user)
                return redirect('manga', manga_id=manga.id)
        else:
            form = VolumeNewForm()
        return render(request, 'web/create.html', {'form': form, 'message': 'Add a volume', 'subnote': manga.name, 'previous': '/manga/' + str(manga.id) + '/'})
    else:
        raise Http404("Page not found")