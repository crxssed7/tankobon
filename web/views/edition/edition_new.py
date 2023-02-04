from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from web.forms import EditionForm

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
