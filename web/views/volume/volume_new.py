from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from api.models import Manga
from web.forms import VolumeForm

@login_required
def new_volume(request, manga_id):
    manga = get_object_or_404(Manga, id=manga_id, locked=False)

    if request.method == "POST":
        data = request.POST.copy()
        data["manga"] = manga.id
        form = VolumeForm(manga, data)
        if form.is_valid():
            v = form.save(commit=False)
            v.manga = manga
            v.locked = False
            v.save()
            return redirect("manga", pk=manga.id)
    else:
        form = VolumeForm(manga=manga)
    return render(
        request,
        "web/create.html",
        {
            "form": form,
            "message": "Add a volume",
            "subnote": manga.name,
            "previous": "/manga/" + str(manga.id) + "/",
        },
    )
