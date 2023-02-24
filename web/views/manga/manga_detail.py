from django.views.generic.detail import DetailView

from api.models import Manga, Edition

class MangaDetailView(DetailView):
    template_name = "web/manga/manga_detail.html"
    context_object_name = "manga"
    model = Manga

    def get_context_data(self, **kwargs):
        context = super(MangaDetailView, self).get_context_data(**kwargs)
        manga = context["manga"]
        editions = Edition.objects.prefetch_related("volume_set").filter(manga=manga).order_by("id")
        user = manga.history.exclude(history_user=None).values("history_user__username").first()
        last_edited_by = None
        if user:
            last_edited_by = user["history_user__username"]

        context.update({"editions": editions, "last_edited_by": last_edited_by})
        return context

    def get_template_names(self):
        if self.request.htmx:
            return ['web/manga/_manga_detail.html']
        return ['web/manga/manga_detail.html']
