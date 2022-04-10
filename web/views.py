from django.shortcuts import render, get_object_or_404
from api.models import Manga, Chapter
from django.views.generic import TemplateView, ListView
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'web/index.html')

def search(request):
    return render(request, 'web/search.html')

class SearchResultsView(ListView):
    model = Manga
    template_name = 'web/search.html'

    def get_queryset(self): # new
        query = self.request.GET.get("q", '')
        if query:
            object_list = Manga.objects.filter(Q(name__icontains=query) | Q(romaji__icontains=query))
        else:
            object_list = Manga.objects.filter(name='')
        return object_list

def detail(request, manga_id):
    manga = get_object_or_404(Manga, id=manga_id)
    chapters = Chapter.objects.filter(manga=manga_id)
    return render(request, 'web/detail.html', context={'manga': manga, 'chapters': chapters})