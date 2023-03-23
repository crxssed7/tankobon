from django.contrib.auth.models import User
from django.views.generic.detail import DetailView

from chartkick.django import PieChart, ColumnChart

from api.models import Volume
from api.extras.stats import Statistics

from tankobon.settings import CHARTKICK_COLORS
from tankobon.utils import get_user_image


class UserDetailView(DetailView):
    model = User
    template_name = "web/users/user_library.html"
    slug_field = "username"
    context_object_name = "object"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context["object"]
        context["avatar"] = get_user_image(user.email)
        collected_volumes = Volume.objects.prefetch_related("edition", "collection_set", "manga").filter(collection__user=user).order_by("edition__manga__name", "absolute_number")

        edition_volumes = {}
        for volume in collected_volumes:
            edition_name = f"{volume.manga} {volume.edition.name} Edition".title()
            if edition_name not in edition_volumes:
                edition_volumes[edition_name] = {'manga': volume.manga, 'volume_list': []}
            edition_volumes[edition_name]['volume_list'].append(volume)
        context["edition_volumes"] = edition_volumes
        return context

    def get_template_names(self):
        if self.request.htmx:
            return ['web/users/_user_library.html']
        return ['web/users/user_library.html']


class UserStatisticsView(DetailView):
    model = User
    template_name = "web/users/user_statistics.html"
    slug_field = "username"
    context_object_name = "object"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context["object"]
        context["avatar"] = get_user_image(user.email)

        stats = Statistics(user).public()
        context["volume_count"] = stats["volume_count"]
        context["monthly_collected"] = ColumnChart(stats["monthly_collected"], colors=CHARTKICK_COLORS)
        context["demographs"] = PieChart(stats["demographs"], colors=CHARTKICK_COLORS)

        return context

    def get_template_names(self):
        if self.request.htmx:
            return ['web/users/_user_statistics.html']
        return ['web/users/user_statistics.html']
