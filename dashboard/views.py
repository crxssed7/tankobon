from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import reverse
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import UpdateView

from chartkick.django import PieChart, ColumnChart

from api.extras.stats import Statistics
from api.models import Collection

from web.forms import CollectionCollectedAtForm, CollectionForm

from tankobon.settings import CHARTKICK_COLORS


# Create your views here.
class DashboardMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["add_collection_form"] = CollectionForm(self.request.user)
        return context

class LibraryView(LoginRequiredMixin, DashboardMixin, ListView):
    model = Collection
    paginate_by = 10
    template_name = "dashboard/library.html"
    context_object_name = "results"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            query = query.strip()
            objects = Collection.objects.prefetch_related("edition", "volume").filter(volume__manga__name__icontains=query, user=self.request.user).order_by("edition__name", "edition__manga__name", "volume__absolute_number")
        else:
            objects = Collection.objects.prefetch_related("edition", "volume").filter(user=self.request.user).order_by("edition__name", "edition__manga__name", "volume__absolute_number")
        return objects

    def get_context_data(self, **kwargs):
        context = super(LibraryView, self).get_context_data(**kwargs)
        q = self.request.GET.get("q")
        if q:
            context["query"] = q
        return context

    def get_template_names(self):
        if self.request.htmx:
            return ["dashboard/_library.html"]
        return ["dashboard/library.html"]

    def post(self, request, *args, **kwargs):
        form = CollectionForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Volume was added to your collection.")
        else:
            messages.add_message(request, messages.ERROR, "Could not add this volume to your collection.")
        return HttpResponseRedirect(redirect_to=reverse("dashboard"))


class CollectionDetailView(LoginRequiredMixin, DashboardMixin, UpdateView):
    template_name = "dashboard/collection.html"
    context_object_name = "collection"
    model = Collection
    form_class = CollectionCollectedAtForm

    def get_template_names(self):
        if self.request.htmx:
            return ['dashboard/_collection.html']
        return ['dashboard/collection.html']

    def get_success_url(self):
        return reverse("collection", kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        collection = self.get_object()
        if collection.user != request.user:
            raise Http404("Collection does not exist.")
        return super().dispatch(request, *args, **kwargs)


class StatisticsView(LoginRequiredMixin, DashboardMixin, TemplateView):
    template_name = "dashboard/statistics.html"

    def get_context_data(self, **kwargs):
        context = super(StatisticsView, self).get_context_data(**kwargs)
        user = self.request.user

        stats = Statistics(user).public()
        context["volume_count"] = stats["volume_count"]
        context["monthly_collected"] = ColumnChart(stats["monthly_collected"], colors=CHARTKICK_COLORS)
        context["demographs"] = PieChart(stats["demographs"], colors=CHARTKICK_COLORS)

        return context
