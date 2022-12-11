from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from api.models import Manga, Volume
from web.forms import VolumeEditForm, VolumeNewForm


@login_required
def edit_volume(request, manga_id, volume_number):
    volume = get_object_or_404(
        Volume, manga=manga_id, absolute_number=volume_number, locked=False
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
        form = VolumeNewForm(data)
        if form.is_valid():
            v = form.save(commit=False)
            v.manga = manga
            v.locked = False
            v.save()
            return redirect("manga", pk=manga.id)
    else:
        form = VolumeNewForm()
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
