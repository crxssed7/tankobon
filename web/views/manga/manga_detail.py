import re

from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

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

def v_json(request, manga_id, edition_language):
    manga_obj = get_object_or_404(Manga, id=manga_id)
    edition = manga_obj.edition_set.filter(language__code=str(edition_language).upper()).first()

    data = {
        "id": manga_obj.anilist_id,
        "volumes": []
    }
    for volume in edition.volume_set.all():
        chapters = volume.chapters.split("\n")
        chapters = list(filter(lambda c: not str(c).startswith("|") and c != '', chapters))
        first_chapter = None
        last_chapter = None

        # ^\w.*(\d+)
        chap1 = re.search(r"(\d+)", chapters[0])
        if chap1 is not None:
            first_chapter = int(chap1.group(1))

        chap2 = re.search(r"(\d+)", chapters[-1])
        if chap2 is not None:
            last_chapter = int(chap2.group(1))

        result = {
            "start": first_chapter,
            "end": last_chapter
        }
        data["volumes"].append(result)
    return JsonResponse(data=data)

def ab_json(request, manga_id, edition_language):
    manga_obj = get_object_or_404(Manga, id=manga_id)
    edition = manga_obj.edition_set.filter(language__code=str(edition_language).upper()).first()

    data = {
        "id": manga_obj.anilist_id,
        "volumes": []
    }
    last_chapter = 0
    for volume in edition.volume_set.all():
        chapters = volume.chapters.split("\n")
        chapters = list(filter(lambda c: not str(c).startswith("|") and c != '', chapters))
        start = last_chapter + 1
        end = last_chapter + len(chapters)

        result = {
            "start": start,
            "end": end
        }
        data["volumes"].append(result)

        last_chapter = end
    return JsonResponse(data=data)
