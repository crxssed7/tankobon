import base64
import textwrap
import requests

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView

from api.models import Manga, Volume
from web.forms import MangaForm


class MangaDetailView(DetailView):
    template_name = "web/detail.html"
    context_object_name = "manga"
    model = Manga

    def get_context_data(self, **kwargs):
        context = super(MangaDetailView, self).get_context_data(**kwargs)
        manga = context["manga"]
        open_vol_request = self.request.GET.get("volume")
        open_vol = -1
        try:
            open_vol = int(open_vol_request)
        except BaseException:
            # If the volume the user provided is not a number, just default to the non tankobon chapters
            open_vol = -1

        volumes = Volume.objects.filter(manga=manga, absolute_number__gte=0).order_by(
            "absolute_number"
        )
        nontankobon = Volume.objects.filter(manga=manga, absolute_number__lt=0).first()
        context.update(
            {
                "data": volumes,
                "chapters_nonvolumed": nontankobon,
                "search_active": "active",
                "open_vol": open_vol,
            }
        )
        return context


class MangaWidgetView(DetailView):
    template_name = "web/widget.svg"
    content_type = "image/svg+xml"
    context_object_name = "manga"
    model = Manga

    def get_context_data(self, **kwargs):
        context = super(MangaWidgetView, self).get_context_data(**kwargs)
        manga = context["manga"]
        title = manga.name
        number = 25
        start = 9.6585464
        # Wraps text so that it looks good in SVG
        wrapper = textwrap.TextWrapper(width=number)
        titles = wrapper.wrap(text=title)
        dic = []
        for i in range(len(titles)):
            _title = {}
            _title["value"] = titles[i]
            _title["step"] = start
            dic.append(_title)
            start += 7

        # Get base64 of image
        poster = ""
        if manga.poster:
            poster = "data:image/png;base64," + base64.b64encode(
                requests.get(manga.poster).content
            ).decode("utf-8")

        context.update({"titles": dic[:5], "poster": poster})
        return context


@login_required
def new_manga(request):
    if request.method == "POST":
        form = MangaForm(request.POST)
        if form.is_valid():
            manga = form.save(commit=False)
            manga.locked = False
            manga.save()
            return redirect("manga", pk=manga.id)
    else:
        form = MangaForm()
    return render(
        request,
        "web/create.html",
        {
            "form": form,
            "message": "Add a manga",
            "previous": "/manga/",
            "type": "manga",
        },
    )


@login_required
def edit_manga(request, manga_id):
    manga_obj = get_object_or_404(Manga, id=manga_id, locked=False)

    if request.method == "POST":
        form = MangaForm(request.POST, instance=manga_obj)
        if form.is_valid():
            manga = form.save()
            return redirect("manga", pk=manga.id)
    else:
        form = MangaForm(instance=manga_obj)
    return render(request, "web/manga_edit.html", {"form": form, "manga": manga_obj})


def all_manga(request):
    manga = Manga.objects.all().order_by("name")[:8]
    manga_count = Manga.objects.count()
    return render(
        request,
        "web/all.html",
        {
            "results": manga,
            "count": manga_count,
            "search_active": "active",
            "type": "all",
        },
    )


def all_manga_completed(request):
    manga = Manga.objects.filter(status="FINISHED").order_by("name")[:8]
    manga_count = Manga.objects.filter(status="FINISHED").count()
    return render(
        request,
        "web/all.html",
        {
            "results": manga,
            "count": manga_count,
            "search_active": "active",
            "type": "completed",
        },
    )


def all_manga_releasing(request):
    manga = Manga.objects.filter(status="RELEASING").order_by("name")[:8]
    manga_count = Manga.objects.filter(status="RELEASING").count()
    return render(
        request,
        "web/all.html",
        {
            "results": manga,
            "count": manga_count,
            "search_active": "active",
            "type": "releasing",
        },
    )
