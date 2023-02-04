from random import sample

from django.db.models import Q
from django.views.generic import ListView

from api.models import Manga

class SearchResultsView(ListView):
    model = Manga
    template_name = "web/manga/manga_search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            object_list = Manga.objects.filter(
                Q(name__icontains=query)
                | Q(romaji__icontains=query)
                | Q(tags__icontains=query)
            )
        else:
            object_list = []
        return object_list

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context["recently_updated"] = Manga.objects.all().order_by("-last_updated")[:8]
        releasing = list(Manga.objects.filter(status="RELEASING"))
        completed = list(Manga.objects.filter(status="FINISHED"))
        context["releasing"] = sample(releasing, 5) if len(releasing) > 5 else releasing
        context["completed"] = sample(completed, 5) if len(completed) > 5 else completed
        q = self.request.GET.get("q")
        if q:
            context["query"] = q
        return context
