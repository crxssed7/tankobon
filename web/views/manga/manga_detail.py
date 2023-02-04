from django.views.generic.detail import DetailView

from api.models import Manga, Edition

class MangaDetailView(DetailView):
    template_name = "web/manga/manga_volumes.html"
    context_object_name = "manga"
    model = Manga

    def get_context_data(self, **kwargs):
        context = super(MangaDetailView, self).get_context_data(**kwargs)
        manga = context["manga"]
        editions = Edition.objects.filter(manga=manga).prefetch_related("volume_set")

        context.update({"editions": editions})
        return context
