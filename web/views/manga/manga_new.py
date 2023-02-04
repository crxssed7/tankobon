from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from web.forms import MangaForm

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
