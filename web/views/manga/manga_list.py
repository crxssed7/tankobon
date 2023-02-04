from django.views.generic import ListView

from api.models import Manga

class ListMangaView(ListView):
    model = Manga
    paginate_by = 14
    template_name = "web/all.html"
    context_object_name = "results"
    ordering = "name"

    def get_context_data(self, **kwargs):
        context = super(ListMangaView, self).get_context_data(**kwargs)
        context["count"] = Manga.objects.count()
        context["search_active"] = "active"
        return context
