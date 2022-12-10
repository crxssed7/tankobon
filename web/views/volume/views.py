from django.shortcuts import render, get_object_or_404, redirect
from api.models import Manga, Volume
from web.forms import VolumeEditForm, VolumeNewForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from tankobon.utils import mongo_log


@login_required
def edit_volume(request, manga_id, volume_number):
    volume = Volume.objects.filter(
        manga=manga_id, absolute_number=volume_number
    ).first()
    if volume:
        if volume.locked == False:
            if request.method == "POST":
                form = VolumeEditForm(request.POST, instance=volume)
                if form.is_valid():
                    v = form.save(commit=False)
                    v.absolute_number = volume.absolute_number
                    v.manga = volume.manga
                    v.save()
                    mongo_log(
                        "Edit Volume",
                        volume.manga.name,
                        str(v) + "\n" + v.chapters,
                        request.user.username,
                    )
                    return redirect("manga", pk=volume.manga.id)
            else:
                form = VolumeEditForm(instance=volume)
            return render(
                request, "web/volume_edit.html", {"form": form, "volume": volume}
            )
        return render(request, "web/volume_edit.html", {"locked": True})
    raise Http404("Page not found")


@login_required
def edit_non_volume(request, manga_id):
    volume = Volume.objects.filter(manga=manga_id, absolute_number__lt=0).first()
    if volume:
        if volume.locked == False:
            if request.method == "POST":
                form = VolumeEditForm(request.POST, instance=volume)
                if form.is_valid():
                    v = form.save(commit=False)
                    v.absolute_number = volume.absolute_number
                    v.manga = volume.manga
                    v.save()
                    mongo_log(
                        "Edit Volume",
                        volume.manga.name,
                        str(v) + "\n" + v.chapters,
                        request.user.username,
                    )
                    return redirect("manga", pk=volume.manga.id)
            else:
                form = VolumeEditForm(instance=volume)
            return render(
                request, "web/volume_edit.html", {"form": form, "volume": volume}
            )
        return render(request, "web/volume_edit.html", {"locked": True})
    raise Http404("Page not found")


@login_required
def new_volume(request, manga_id):
    manga = get_object_or_404(Manga, id=manga_id)
    if not manga.locked:
        if request.method == "POST":
            data = request.POST.copy()
            data["manga"] = manga.id
            form = VolumeNewForm(data)
            if form.is_valid():
                v = form.save(commit=False)
                v.manga = manga
                v.locked = False
                v.save()
                mongo_log(
                    "New Volume",
                    manga.name,
                    str(v) + "\n" + v.chapters,
                    request.user.username,
                )
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
    raise Http404("Page not found")
