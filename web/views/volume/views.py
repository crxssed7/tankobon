from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from api.models import Manga, Volume, Edition
from web.forms import VolumeEditForm, VolumeNewForm


@login_required
def edit_volume(request, manga_id, volume_number):
    _edition = request.GET.get("edition")
    if _edition:
        edition = Edition.objects.filter(name=_edition.lower(), manga=manga_id).first()
    else:
        edition = Edition.objects.filter(name="standard", manga=manga_id).first()

    if not edition:
        raise Http404("This edition does not exist")

    volume = get_object_or_404(
        Volume,
        manga=manga_id,
        absolute_number=volume_number,
        locked=False,
        edition=edition,
    )

    if request.method == "POST":
        form = VolumeEditForm(request.POST, instance=volume)
        if form.is_valid():
            v = form.save(commit=False)
            v.absolute_number = volume.absolute_number
            v.manga = volume.manga
            v.save()
            return redirect("manga", pk=volume.manga.id)
    else:
        form = VolumeEditForm(instance=volume)
    return render(request, "web/volume_edit.html", {"form": form, "volume": volume})


@login_required
def new_volume(request, manga_id):
    manga = get_object_or_404(Manga, id=manga_id, locked=False)

    if request.method == "POST":
        data = request.POST.copy()
        data["manga"] = manga.id
        form = VolumeNewForm(manga, data)
        if form.is_valid():
            v = form.save(commit=False)
            v.manga = manga
            v.locked = False
            v.save()
            return redirect("manga", pk=manga.id)
    else:
        form = VolumeNewForm(manga=manga)
    return render(
        request,
        "web/create.html",
        {
            "form": form,
            "message": "Add a volume",
            "subnote": manga.name,
            "previous": "/manga/" + str(manga.id) + "/",
            "type": "volume",
        },
    )
