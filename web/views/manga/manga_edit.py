from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from api.models import Manga
from web.forms import MangaForm

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
