from django.shortcuts import render, get_object_or_404
from api.models import Manga, Chapter
from django.views.generic import TemplateView, ListView
from django.db.models import Q, Count

# Create your views here.
def index(request):
    return render(request, 'web/index.html', context={'home_active': 'active'})

class SearchResultsView(ListView):
    model = Manga
    template_name = 'web/search.html'

    def get_queryset(self): # new
        query = self.request.GET.get("q")
        if query:
            object_list = Manga.objects.filter(Q(name__icontains=query) | Q(romaji__icontains=query))
        else:
            object_list = Manga.objects.all().order_by('-id')[:4]
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
    chapters_volumed = Chapter.objects.filter(manga=manga_id, volume__gte=0).order_by('chapter_number').order_by('volume')

    print(chapters_volumed)

    # Garbage, hard to read fuck it
    data = []
    current = 1
    chapters = []
    chapter_count = len(chapters_volumed)
    for i in range(chapter_count):
        print('Index: ' + str(i))
        print('Current chapter: ' + str(chapters_volumed[i]))

        tmp = {'volume': current}

        if current != chapters_volumed[i].volume:
            current = chapters_volumed[i].volume
            tmp.update({'chapters': chapters})
            data.append(tmp)
            chapters = []
            
        chapters.append(chapters_volumed[i])

        if i == chapter_count - 1:
            current = chapters_volumed[i].volume
            tmp = {'volume': current}
            tmp.update({'chapters': chapters})
            data.append(tmp)

    chapters_nonvolumed = Chapter.objects.filter(manga=manga_id, volume__lt=0).order_by('chapter_number')
    return render(request, 'web/detail.html', context={'manga': manga, 'data': data, 'chapters_nonvolumed': chapters_nonvolumed})