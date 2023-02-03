from random import sample

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView

from api.models import Manga, Edition
from web.forms import SignUpForm, LoginForm


class IndexView(TemplateView):
    template_name = "web/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["home_active"] = "active"
        return context


class HelpNeededView(TemplateView):
    template_name = "web/help.html"

    def get_context_data(self, **kwargs):
        context = super(HelpNeededView, self).get_context_data(**kwargs)
        context["no_volume"] = (
            Edition.objects.select_related("manga").annotate(cnt=Count("volume"))
            .filter(cnt=0)
        )
        context["no_poster"] = Manga.objects.filter(poster_file="")
        context["no_genre"] = (
            Manga.objects.all().annotate(cnt=Count("genres")).filter(cnt=0)
        )
        return context


class SearchResultsView(ListView):
    model = Manga
    template_name = "web/search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            object_list = Manga.objects.filter(
                Q(name__icontains=query)
                | Q(romaji__icontains=query)
                | Q(tags__icontains=query)
            )
        else:
            object_list = []
        return object_list

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context["recently_updated"] = Manga.objects.all().order_by("-last_updated")[:8]
        releasing = list(Manga.objects.filter(status="RELEASING"))
        completed = list(Manga.objects.filter(status="FINISHED"))
        context["releasing"] = sample(releasing, 5) if len(releasing) > 5 else releasing
        context["completed"] = sample(completed, 5) if len(completed) > 5 else completed
        context["search_active"] = "active"
        q = self.request.GET.get("q")
        if q:
            context["query"] = q
        return context


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class GuidelinesView(TemplateView):
    template_name = "web/contrib.html"


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse("search"))
        else:
            messages.error(request, "Username or password not correct")
            return redirect(reverse("login"))
    else:
        form = LoginForm()
    rendered_form = form.render("web/form_snippet.html")
    return render(request, "registration/login.html", {"form": rendered_form})
