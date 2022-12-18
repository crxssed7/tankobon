import base64
import textwrap
import requests

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from api.models import Manga, Edition
from web.forms import MangaForm, EditionForm


class MangaDetailView(DetailView):
    template_name = "web/manga_volumes.html"
    context_object_name = "manga"
    model = Manga

    def get_context_data(self, **kwargs):
        context = super(MangaDetailView, self).get_context_data(**kwargs)
        manga = context["manga"]
        editions = Edition.objects.filter(manga=manga).prefetch_related("volume_set")

        context.update({"search_active": "active", "editions": editions})
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


class ListMangaView(ListView):
    model = Manga
    template_name = "web/all.html"
    context_object_name = "results"

    def get_queryset(self):
        status = str(self.request.GET.get("status")).lower()
        choices = ["releasing", "finished"]
        if status not in choices:
            # We need to get all manga.
            queryset = Manga.objects.all().order_by("name")[:8]
        else:
            queryset = Manga.objects.filter(status=status.upper()).order_by("name")[:8]
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListMangaView, self).get_context_data(**kwargs)
        status = str(self.request.GET.get("status")).lower()
        choices = ["releasing", "finished"]
        if status not in choices:
            context["count"] = Manga.objects.count()
            context["type"] = "all"
        else:
            context["count"] = Manga.objects.filter(status=status.upper()).count()
            context["type"] = status
        context["search_active"] = "active"
        return context


@login_required
def new_edition(request):
    if request.method == "POST":
        form = EditionForm(request.POST)
        if form.is_valid():
            edition = form.save(commit=True)
            return redirect("manga", pk=edition.manga.id)
    else:
        form = EditionForm()
    return render(
        request,
        "web/create.html",
        {
            "form": form,
            "message": "Add an edition",
            "previous": "/manga/",
        },
    )
