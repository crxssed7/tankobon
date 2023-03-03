from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from api.models import Collection

# Create your views here.
class LibraryView(LoginRequiredMixin, ListView):
    model = Collection
    paginate_by = 10
    template_name = "dashboard/library.html"
    context_object_name = "results"
    ordering = ["edition__manga__name", "volume__absolute_number"]

    def get_template_names(self):
        if self.request.htmx:
            return ["dashboard/_library.html"]
        return ["dashboard/library.html"]


class CollectionDetailView(LoginRequiredMixin, DetailView):
    template_name = "dashboard/collection.html"
    context_object_name = "collection"
    model = Collection

    def get_template_names(self):
        if self.request.htmx:
            return ['dashboard/_collection.html']
        return ['dashboard/collection.html']
