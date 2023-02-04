from django.db.models import Count
from django.views.generic import TemplateView

from api.models import Manga, Edition


class IndexView(TemplateView):
    template_name = "web/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["home_active"] = "active"
        return context


class HelpNeededView(TemplateView):
    template_name = "web/help.html"

    def get_context_data(self, **kwargs):
        context = super(HelpNeededView, self).get_context_data(**kwargs)
        context["no_volume"] = (
            Edition.objects.select_related("manga").annotate(cnt=Count("volume"))
            .filter(cnt=0)
        )
        context["no_poster"] = Manga.objects.filter(poster_file="")
        context["no_genre"] = (
            Manga.objects.all().annotate(cnt=Count("genres")).filter(cnt=0)
        )
        return context
