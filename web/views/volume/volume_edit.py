from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from api.models import Volume, Edition
from web.forms import VolumeEditForm

@login_required
def edit_volume(request, manga_id, volume_number):
    _edition = request.GET.get("edition")
    edition = None
    if _edition:
        edition = Edition.objects.filter(name=_edition.lower(), manga=manga_id).first()

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
    return render(request, "web/volume/volume_edit.html", {"form": form, "volume": volume})
